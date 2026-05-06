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
    """Return a list of {old_start, old_count} for each hunk in a .rej file."""
    hunks: list[dict] = []
    for line in content.splitlines():
        m = HUNK_HEADER_RE.match(line)
        if m:
            hunks.append({
                "old_start": int(m.group(1)),
                "old_count": int(m.group(2)) if m.group(2) else 1,
            })
    return hunks


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

    for rej in rejects:
        target = rej[:-4]
        rel = os.path.relpath(target, node_dir)
        with open(rej, encoding="utf-8", errors="ignore") as f:
            rej_content = f.read()
        hunks = parse_rej(rej_content)

        parts.append(f"================ REJECT: {rel} ================")
        parts.append(rej_content.rstrip())
        parts.append("")
        parts.append(f"---- current content of {rel} ----")
        if not hunks:
            # Couldn't parse any hunk header — show a small head of the file.
            parts.append(file_section(target, 1, 1))
        else:
            for h in hunks:
                parts.append(f"# around line {h['old_start']}:")
                parts.append(file_section(target, h["old_start"], h["old_count"]))
                parts.append("")
        parts.append("")

    with open(prompt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print(f"Prepared prompt for {len(rejects)} reject file(s) -> {prompt_path}")


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

    blocks = list(BLOCK_RE.finditer(response))
    print(f"Parsed {len(blocks)} search/replace block(s) from AI response")

    failed: list[str] = []
    touched: set[str] = set()

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
        touched.add(rel)
        print(f"✅ {rel}: applied resolution")

    # Drop .rej files for targets that were fully covered without failures.
    failed_set = set(failed)
    for rej in initial_rejects:
        rel = os.path.relpath(rej[:-4], node_dir)
        if rel in touched and rel not in failed_set:
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
