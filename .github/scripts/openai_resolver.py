#!/usr/bin/env python3
import sys
import json
import os
from urllib.request import Request, urlopen
from urllib.parse import urlencode


def call_openai_api(prompt, api_key, model="gpt-3.5-turbo"):
    """Call OpenAI API to resolve patch conflicts"""
    url = "https://api.openai.com/v1/chat/completions"

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    data = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are an expert C++ developer helping to resolve Git patch conflicts. Return only the corrected file content without explanations or markdown formatting.",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.1,
        "max_tokens": 4000,
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
        print(f"OpenAI API error: {e}", file=sys.stderr)
        return None


def resolve_conflict(reject_file, original_file, api_key):
    """Resolve a single conflict using OpenAI"""

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

    # Create prompt for OpenAI
    prompt = f"""I have a Git patch that failed to apply to a Node.js C++ source file. 

REJECTED PATCH HUNKS:
```
{reject_content}
```

CURRENT FILE CONTENT:
```
{current_content}
```

Please analyze the rejected patch hunks and the current file content, then provide the complete corrected file content that successfully applies the intended changes from the patch. The changes should:

1. Apply the intended modifications from the rejected hunks
2. Handle any line number shifts or context changes
3. Maintain proper C++ syntax and formatting
4. Preserve existing functionality while adding the patch changes

Return ONLY the complete corrected file content, no explanations."""

    print(f"Calling OpenAI API to resolve {original_file}...", file=sys.stderr)

    resolved_content = call_openai_api(prompt, api_key)

    if resolved_content:
        try:
            # Write resolved content
            with open(original_file, "w", encoding="utf-8") as f:
                f.write(resolved_content)
            print(f"✅ Successfully resolved {original_file}")
            return True
        except Exception as e:
            print(
                f"Error writing resolved content to {original_file}: {e}",
                file=sys.stderr,
            )
            return False
    else:
        print(f"❌ Failed to get resolution from OpenAI for {original_file}")
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
