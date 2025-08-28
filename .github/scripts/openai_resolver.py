#!/usr/bin/env python3
import sys
import json
import os
import re
from urllib.request import Request, urlopen


def parse_reject_file(reject_content):
    """Parse reject file to extract hunk information"""
    hunks = []
    lines = reject_content.split("\n")

    current_hunk = None
    for line in lines:
        # Match hunk header: @@ -start,count +start,count @@
        hunk_match = re.match(r"@@\s*-(\d+)(?:,(\d+))?\s*\+(\d+)(?:,(\d+))?\s*@@", line)
        if hunk_match:
            old_start = int(hunk_match.group(1))
            old_count = int(hunk_match.group(2)) if hunk_match.group(2) else 1
            new_start = int(hunk_match.group(3))
            new_count = int(hunk_match.group(4)) if hunk_match.group(4) else 1

            current_hunk = {
                "old_start": old_start,
                "old_count": old_count,
                "new_start": new_start,
                "new_count": new_count,
                "lines": [],
            }
            hunks.append(current_hunk)
        elif current_hunk is not None and (
            line.startswith(" ") or line.startswith("-") or line.startswith("+")
        ):
            current_hunk["lines"].append(line)

    return hunks


def extract_file_context(file_content, hunks, context_lines=5):
    """Extract relevant sections from file based on hunks"""
    if not file_content:
        return ""

    file_lines = file_content.split("\n")
    extracted_sections = []

    for hunk in hunks:
        # Calculate the range of lines to extract with extra context
        start_line = max(
            0, hunk["old_start"] - context_lines - 1
        )  # -1 for 0-based indexing
        end_line = min(
            len(file_lines), hunk["old_start"] + hunk["old_count"] + context_lines - 1
        )

        # Extract the section
        section_lines = file_lines[start_line:end_line]
        section = {
            "start_line_num": start_line + 1,  # Convert back to 1-based for display
            "end_line_num": end_line,
            "content": "\n".join(section_lines),
            "hunk": hunk,
        }
        extracted_sections.append(section)

    return extracted_sections


def apply_fixed_sections(original_content, fixed_sections):
    """Apply fixed sections back to the original file"""
    if not original_content:
        return fixed_sections[0]["content"] if fixed_sections else ""

    file_lines = original_content.split("\n")

    # Sort sections by start line (descending) to apply from bottom to top
    sorted_sections = sorted(
        fixed_sections, key=lambda x: x["start_line_num"], reverse=True
    )

    for section in sorted_sections:
        start_idx = section["start_line_num"] - 1  # Convert to 0-based indexing
        end_idx = section["end_line_num"]

        # Replace the section
        fixed_lines = section["content"].split("\n")
        file_lines[start_idx:end_idx] = fixed_lines

    return "\n".join(file_lines)


def call_openai_api(prompt, api_key, model="gpt-3.5-turbo"):
    """Call OpenAI API to resolve patch conflicts"""
    url = "https://api.openai.com/v1/chat/completions"

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    data = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are an expert C++/JS developer helping to resolve Git patch conflicts. Return only the corrected code section without explanations or markdown formatting. Preserve the exact number of lines and structure.",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.1,
        "max_tokens": 1000,
    }

    try:
        req = Request(url, data=json.dumps(data).encode("utf-8"), headers=headers)
        with urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"].strip()
            else:
                return None
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return None


def resolve_conflict(reject_file, original_file, api_key):
    """Resolve a single conflict using OpenAI with context extraction"""

    # Read reject file content
    try:
        with open(reject_file, "r", encoding="utf-8", errors="ignore") as f:
            reject_content = f.read()
    except Exception as e:
        print(f"Error reading reject file {reject_file}: {e}", file=sys.stderr)
        return False

    # Read current file content
    current_content = ""
    if os.path.exists(original_file):
        try:
            with open(original_file, "r", encoding="utf-8", errors="ignore") as f:
                current_content = f.read()
        except Exception as e:
            print(f"Error reading original file {original_file}: {e}", file=sys.stderr)

    # Parse reject file to extract hunks
    hunks = parse_reject_file(reject_content)
    if not hunks:
        print(f"No valid hunks found in {reject_file}", file=sys.stderr)
        return False

    # Extract relevant file sections
    file_sections = extract_file_context(current_content, hunks)

    fixed_sections = []

    # Process each section
    for i, section in enumerate(file_sections):
        hunk = section["hunk"]

        # Create prompt for this specific section
        prompt = f"""I have a Git patch that failed to apply. Here's the specific section that needs to be fixed:

REJECTED PATCH HUNK:
```
@@ -{hunk['old_start']},{hunk['old_count']} +{hunk['new_start']},{hunk['new_count']} @@
{chr(10).join(hunk['lines'])}
```

CURRENT FILE SECTION (lines {section['start_line_num']}-{section['end_line_num']}):
```
{section['content']}
```

Please apply the intended changes from the rejected hunk to this file section. Return ONLY the corrected file section content, preserving the exact line structure and formatting. Do not add explanations or markdown formatting."""

        print(
            f"Processing section {i+1}/{len(file_sections)} for {original_file}...",
            file=sys.stderr,
        )

        print(f"Prompt for OpenAI API:\n{prompt}")

        resolved_content = call_openai_api(prompt, api_key)

        if resolved_content:
            fixed_sections.append(
                {
                    "start_line_num": section["start_line_num"],
                    "end_line_num": section["end_line_num"],
                    "content": resolved_content,
                }
            )
        else:
            print(f"❌ Failed to get resolution from OpenAI for section {i+1}")
            return False

    # Apply all fixed sections back to the original file
    try:
        final_content = apply_fixed_sections(current_content, fixed_sections)
        with open(original_file, "w", encoding="utf-8") as f:
            f.write(final_content)
        print(f"✅ Successfully resolved {original_file}")
        return True
    except Exception as e:
        print(
            f"Error writing resolved content to {original_file}: {e}", file=sys.stderr
        )
        return False


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            "Usage: openai_resolver.py <reject_files_dir> <api_key>",
            file=sys.stderr,
        )
        sys.exit(1)

    reject_dir = sys.argv[1]
    api_key = sys.argv[2]

    # Find all .rej files
    reject_files = []
    for root, dirs, files in os.walk(reject_dir):
        for file in files:
            if file.endswith(".rej"):
                reject_files.append(os.path.join(root, file))

    if not reject_files:
        print("No reject files found")
        sys.exit(0)

    conflicts_resolved = 0
    total_conflicts = len(reject_files)
    failed_files = []

    print(f"Found {total_conflicts} reject files to process")

    for reject_file in reject_files:
        original_file = reject_file[:-4]  # Remove .rej extension
        print(f"Processing: {reject_file} -> {original_file}")

        if resolve_conflict(reject_file, original_file, api_key):
            conflicts_resolved += 1
        else:
            print(f"Failed to resolve {original_file}")
            failed_files.append(original_file)
            break

        # Clean up reject file
        try:
            os.remove(reject_file)
        except:
            pass

    # Output results for GitHub Actions
    print(f"CONFLICTS_RESOLVED={conflicts_resolved}")
    print(f"TOTAL_CONFLICTS={total_conflicts}")
    print(f"HAS_UNRESOLVED={failed_files.__len__() > 0}")

    if failed_files:
        print("FAILED_FILES=", " ".join(failed_files))

    print(
        f"Resolution summary: {conflicts_resolved}/{total_conflicts} conflicts resolved"
    )

    # Exit with appropriate code
    sys.exit(0 if conflicts_resolved == total_conflicts else 1)
