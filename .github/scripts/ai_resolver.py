#!/usr/bin/env python3
"""Resolve `git apply --reject` rejections with the help of an LLM.

Two subcommands:

  prepare <node_dir> <prompt_file>
      Walk *.rej files under <node_dir>, build a single prompt that asks the
      model for a search/replace block per rejected hunk, write it to
      <prompt_file>.

  apply <node_dir> <response_file>
      Parse search/replace blocks from <response_file>, apply them to the
      corresponding files under <node_dir>, delete the .rej files that were
      successfully resolved, and print GitHub Actions env-style summary lines:

          CONFLICTS_RESOLVED=<n>
          TOTAL_CONFLICTS=<n>
          HAS_UNRESOLVED=<True|False>
          FAILED_FILES=<space-separated paths>   (only when there are any)

      Exits 0 on full success, 1 if anything is unresolved.

The output protocol the model must follow (and that `apply` parses):

    === FILE: <relative/path> ===
    <<<<<<< SEARCH
    <exact text currently in the file>
    =======
    <replacement text>
    >>>>>>> REPLACE

Multiple blocks per file are allowed; each SEARCH must match the file's
current content verbatim (after the partial `git apply --reject` has run).
"""

from __future__ import annotations

import os
import re
import sys

# How many lines of surrounding context we hand to the model per rejected
# hunk. Big enough to disambiguate SEARCH targets, small enough to keep the
# prompt within the model's context window for a multi-reject patch.
CONTEXT_LINES = 15

HUNK_HEADER_RE = re.compile(r"@@\s*-(\d+)(?:,(\d+))?\s*\+\d+(?:,\d+)?\s*@@")

BLOCK_RE = re.compile(
    r"^=== FILE: (?P<file>.+?) ===[ \t]*$\n"
    r"^<<<<<<< SEARCH[ \t]*$\n"
    r"(?P<search>.*?)\n"
    r"^=======[ \t]*$\n"
    r"(?P<replace>.*?)\n"
    r"^>>>>>>> REPLACE[ \t]*$",
    re.DOTALL | re.MULTILINE,
)


def find_reject_files(root: str) -> list[str]:
    out: list[str] = []
    for dp, _, files in os.walk(root):
        for f in files:
            if f.endswith(".rej"):
                out.append(os.path.join(dp, f))
    out.sort()
    return out


def parse_rej(content: str) -> list[dict]:
    """Return a list of hunks for each hunk in a .rej file.

    Each hunk is ``{old_start, old_count, header, lines}`` where ``header`` is
    the raw ``@@ … @@`` line and ``lines`` holds the raw body lines (each still
    carrying its leading ' ', '-', '+' or '\\' tag) so callers can reconstruct
    both the hunk text and the pre-/post-image of the change.
    """
    hunks: list[dict] = []
    current: dict | None = None
    for line in content.splitlines():
        m = HUNK_HEADER_RE.match(line)
        if m:
            current = {
                "old_start": int(m.group(1)),
                "old_count": int(m.group(2)) if m.group(2) else 1,
                "header": line,
                "lines": [],
            }
            hunks.append(current)
        elif current is not None:
            # A new file header means the previous hunk's body is over.
            # .rej files normally hold a single file, but be defensive.
            if line.startswith(("--- ", "+++ ", "diff ")):
                current = None
                continue
            current["lines"].append(line)
    return hunks


def _hunk_images(hunk: dict) -> tuple[list[str], list[str]]:
    """Split a hunk body into its (pre-image, post-image) file lines.

    Pre-image = context + removed lines (what the file looked like BEFORE the
    patch). Post-image = context + added lines (what it looks like AFTER).
    """
    pre: list[str] = []
    post: list[str] = []
    for ln in hunk["lines"]:
        if ln == "":
            # A blank context line is normally " "; tolerate a bare "".
            pre.append("")
            post.append("")
            continue
        tag, text = ln[0], ln[1:]
        if tag == " ":
            pre.append(text)
            post.append(text)
        elif tag == "-":
            pre.append(text)
        elif tag == "+":
            post.append(text)
        elif tag == "\\":
            # "\ No newline at end of file" marker — not file content.
            continue
        else:
            # Unexpected prefix; keep it verbatim on both sides.
            pre.append(ln)
            post.append(ln)
    return pre, post


def _block_in(file_lines: list[str], block: list[str]) -> bool:
    """True if `block` appears as a contiguous run within `file_lines`."""
    if not block:
        return False
    n, m = len(file_lines), len(block)
    for i in range(n - m + 1):
        if file_lines[i:i + m] == block:
            return True
    return False


def hunk_already_applied(file_lines: list[str], hunk: dict) -> bool:
    """True if `hunk`'s change is already present in `file_lines`.

    This is the common case where upstream independently landed the same edit
    the patch carries (e.g. a Node.js release that merged the fix). The hunk's
    post-image is in the file and its pre-image is gone, so there is nothing to
    resolve — the regenerated patch should simply omit the hunk.
    """
    pre, post = _hunk_images(hunk)
    return _block_in(file_lines, post) and not _block_in(file_lines, pre)


def classify_hunks(target_path: str, hunks: list[dict]) -> tuple[list[dict], list[dict]]:
    """Partition hunks into (already_applied, pending) for `target_path`.

    The file is read once here and shared across every hunk check.
    """
    if not os.path.isfile(target_path):
        # No file to compare against — treat every hunk as still pending.
        return [], list(hunks)
    with open(target_path, encoding="utf-8", errors="ignore") as f:
        file_lines = f.read().splitlines()
    already: list[dict] = []
    pending: list[dict] = []
    for h in hunks:
        (already if hunk_already_applied(file_lines, h) else pending).append(h)
    return already, pending


def file_section(path: str, start: int, count: int) -> str:
    """Return the file slice around [start, start+count) with extra context."""
    if not os.path.exists(path):
        return ""
    with open(path, encoding="utf-8", errors="ignore") as f:
        lines = f.read().splitlines()
    lo = max(0, start - CONTEXT_LINES - 1)
    hi = min(len(lines), start + count + CONTEXT_LINES - 1)
    numbered = (f"{i + 1:6d}  {lines[i]}" for i in range(lo, hi))
    return "\n".join(numbered)


def cmd_prepare(node_dir: str, prompt_path: str) -> None:
    rejects = find_reject_files(node_dir)
    if not rejects:
        # Nothing to do — write an empty prompt and exit cleanly. The workflow
        # gates the AI step on rejects existing, so this branch is defensive.
        open(prompt_path, "w", encoding="utf-8").close()
        print("No reject files found")
        return

    parts: list[str] = [
        "You are resolving Git patch rejections (`.rej` files produced by "
        "`git apply --reject`) against a freshly-checked-out Node.js source "
        "tree. The patch was authored against an older Node.js release; the "
        "rejected hunks must be re-expressed so they apply to the new tree "
        "while preserving the original patch's intent.",
        "",
        "For every rejected hunk, emit ONE search/replace block in EXACTLY "
        "this format (no markdown fences, no commentary, no leading prose):",
        "",
        "=== FILE: <path relative to the node source root> ===",
        "<<<<<<< SEARCH",
        "<verbatim text that currently exists in the file>",
        "=======",
        "<text that should replace it>",
        ">>>>>>> REPLACE",
        "",
        "Rules:",
        "  - SEARCH must match the file's CURRENT content byte-for-byte "
        "(whitespace, indentation, trailing punctuation included).",
        "  - Keep SEARCH minimal but unambiguous — include enough surrounding "
        "lines that it appears exactly once in the file.",
        "  - REPLACE is what the file should look like after applying the "
        "patch's intent.",
        "  - Multiple blocks per file are fine. Order does not matter.",
        "  - Do not wrap the output in ``` fences. Do not add explanations.",
        "",
        "Below is each rejected hunk together with the relevant slice of the "
        "current file (line numbers shown for orientation only — do not "
        "include them in SEARCH/REPLACE).",
        "",
    ]

    prompted = 0
    for rej in rejects:
        target = rej[:-4]
        rel = os.path.relpath(target, node_dir)
        with open(rej, encoding="utf-8", errors="ignore") as f:
            rej_content = f.read()
        hunks = parse_rej(rej_content)

        # Drop hunks that upstream already applied — there is nothing for the
        # model to resolve, and asking it to would only invite a hallucinated
        # SEARCH block that fails to match. The `apply` step recognises these
        # the same way and lets the .rej be cleared without an AI block.
        already, pending = classify_hunks(target, hunks)
        if already:
            print(f"ℹ️ {rel}: {len(already)}/{len(hunks)} hunk(s) already applied upstream — skipping")
        if hunks and not pending:
            # Whole file is already upstream; nothing to send to the model.
            continue

        prompted += 1
        parts.append(f"================ REJECT: {rel} ================")
        if not hunks:
            # Couldn't parse any hunk header — fall back to the raw .rej body
            # plus a small head of the file.
            parts.append(rej_content.rstrip())
            parts.append("")
            parts.append(f"---- current content of {rel} ----")
            parts.append(file_section(target, 1, 1))
            parts.append("")
            continue

        # Show ONLY the pending hunks. Including already-applied hunks here —
        # while the system prompt says "emit a block for every rejected hunk" —
        # would push the model to produce a doomed block for them, which fails
        # to apply and keeps the .rej around. The model never sees them.
        for h in pending:
            parts.append(h["header"])
            parts.extend(h["lines"])
            parts.append("")
        parts.append(f"---- current content of {rel} ----")
        for h in pending:
            parts.append(f"# around line {h['old_start']}:")
            parts.append(file_section(target, h["old_start"], h["old_count"]))
            parts.append("")
        parts.append("")

    with open(prompt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print(f"Prepared prompt for {prompted}/{len(rejects)} reject file(s) -> {prompt_path}")


def _strip_outer_fence(text: str) -> str:
    """Remove a single outer ```...``` fence if the model wrapped its reply."""
    text = text.strip()
    m = re.match(r"^```[\w-]*\s*\n(.*)\n```\s*$", text, re.DOTALL)
    return m.group(1) if m else text


def cmd_apply(node_dir: str, response_path: str) -> None:
    with open(response_path, encoding="utf-8") as f:
        response = _strip_outer_fence(f.read())

    initial_rejects = find_reject_files(node_dir)
    total = len(initial_rejects)

    # Count the hunks the AI must resolve per file BEFORE applying anything.
    # Hunks upstream already landed are excluded — the file already carries
    # their post-image, so no SEARCH/REPLACE block is expected (or possible)
    # for them. The AI must return at least one successfully-applying block
    # per *pending* hunk; otherwise we'd silently drop unaddressed hunks when
    # the .rej is deleted at the end.
    expected_per_file: dict[str, int] = {}
    for rej in initial_rejects:
        target = rej[:-4]
        rel = os.path.relpath(target, node_dir)
        with open(rej, encoding="utf-8", errors="ignore") as f:
            hunks = parse_rej(f.read())
        already, pending = classify_hunks(target, hunks)
        if already:
            print(f"ℹ️ {rel}: {len(already)}/{len(hunks)} hunk(s) already applied upstream — skipping")
        expected_per_file[rel] = len(pending)

    blocks = list(BLOCK_RE.finditer(response))
    print(f"Parsed {len(blocks)} search/replace block(s) from AI response")

    failed: list[str] = []
    applied_per_file: dict[str, int] = {}

    for m in blocks:
        rel = m.group("file").strip()
        path = os.path.join(node_dir, rel)
        search = m.group("search")
        replace = m.group("replace")

        if not os.path.isfile(path):
            print(f"❌ {rel}: file does not exist")
            failed.append(rel)
            continue

        with open(path, encoding="utf-8") as f:
            content = f.read()

        occurrences = content.count(search)
        if occurrences == 0:
            print(f"❌ {rel}: SEARCH block not found in current file")
            failed.append(rel)
            continue
        if occurrences > 1:
            print(f"❌ {rel}: SEARCH block is ambiguous ({occurrences} matches)")
            failed.append(rel)
            continue

        with open(path, "w", encoding="utf-8") as f:
            f.write(content.replace(search, replace, 1))
        applied_per_file[rel] = applied_per_file.get(rel, 0) + 1
        expected = expected_per_file.get(rel, "?")
        print(f"✅ {rel}: applied resolution ({applied_per_file[rel]}/{expected})")

    # Delete .rej only when EVERY rejected hunk in that file has been
    # addressed by a successfully-applying block. Files where the AI
    # returned fewer blocks than there were hunks (or where any block
    # failed to apply) keep their .rej, so the leftover scan below
    # flags them as unresolved and the workflow aborts before PR.
    failed_set = set(failed)
    for rej in initial_rejects:
        rel = os.path.relpath(rej[:-4], node_dir)
        expected = expected_per_file[rel]
        applied = applied_per_file.get(rel, 0)
        if rel in failed_set:
            print(f"⚠️ {rel}: kept .rej — at least one block failed to apply")
            continue
        if applied < expected:
            print(f"⚠️ {rel}: kept .rej — AI returned {applied}/{expected} blocks")
            continue
        try:
            os.remove(rej)
        except OSError:
            pass

    leftover = [
        os.path.relpath(r[:-4], node_dir)
        for r in find_reject_files(node_dir)
    ]
    has_unresolved = bool(leftover) or bool(failed)
    resolved = total - len(leftover)

    print(f"CONFLICTS_RESOLVED={resolved}")
    print(f"TOTAL_CONFLICTS={total}")
    print(f"HAS_UNRESOLVED={'True' if has_unresolved else 'False'}")
    if leftover or failed:
        merged = sorted(set(leftover) | failed_set)
        print(f"FAILED_FILES={' '.join(merged)}")
    print(f"Resolution summary: {resolved}/{total} conflicts resolved")

    sys.exit(0 if not has_unresolved else 1)


def main() -> None:
    if len(sys.argv) != 4 or sys.argv[1] not in ("prepare", "apply"):
        print(
            "Usage:\n"
            "  ai_resolver.py prepare <node_dir> <prompt_file>\n"
            "  ai_resolver.py apply   <node_dir> <response_file>",
            file=sys.stderr,
        )
        sys.exit(2)

    cmd, node_dir, payload = sys.argv[1], sys.argv[2], sys.argv[3]
    if cmd == "prepare":
        cmd_prepare(node_dir, payload)
    else:
        cmd_apply(node_dir, payload)


if __name__ == "__main__":
    main()
