#!/usr/bin/env python3
"""Validate a review and enforce its severity. Exit 0 pass, 1 blocking, 2 invalid."""
import argparse
import html
import json
import os
import sys
from pathlib import Path, PurePosixPath

RULES = {f"PAY-{i:03d}" for i in range(1, 6)}


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def validate(review):
    if not isinstance(review, dict) or set(review) != {"summary", "findings"}:
        raise ValueError("expected exactly summary and findings")
    if not nonempty(review["summary"]) or not isinstance(review["findings"], list):
        raise ValueError("invalid summary or findings")
    for finding in review["findings"]:
        fields = {"severity", "rule", "file", "line", "message"}
        if not isinstance(finding, dict) or set(finding) != fields:
            raise ValueError("invalid finding fields")
        if finding["severity"] not in ("blocking", "advisory"):
            raise ValueError("invalid severity")
        if not isinstance(finding["rule"], str) or finding["rule"] not in RULES:
            raise ValueError("invalid policy rule")
        if not nonempty(finding["file"]) or not nonempty(finding["message"]):
            raise ValueError("file and message are required")
        path = PurePosixPath(finding["file"])
        if path.is_absolute() or ".." in path.parts or "\\" in finding["file"]:
            raise ValueError("file must be repository-relative")
        if type(finding["line"]) is not int or finding["line"] < 1:
            raise ValueError("line must be a positive integer")
    return review


def no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("review", type=Path)
    parser.add_argument("--prepared", action="store_true", help="Clearly label a rehearsal fixture")
    args = parser.parse_args()
    label = "PREPARED REHEARSAL FIXTURE — not a live Codex review" if args.prepared else "Codex policy gate"
    try:
        review = validate(json.loads(args.review.read_text(), object_pairs_hook=no_duplicate_keys))
    except (OSError, ValueError, TypeError) as error:
        print(f"{label}: INVALID REVIEW — {error}", file=sys.stderr)
        return 2
    blocking = sum(f["severity"] == "blocking" for f in review["findings"])
    advisory = len(review["findings"]) - blocking
    print(label)
    print(review["summary"])
    for finding in review["findings"]:
        print(f"{finding['severity'].upper()} {finding['rule']} {finding['file']}:{finding['line']} — {finding['message']}")
    print(f"{'FAIL' if blocking else 'PASS'}: {blocking} blocking, {advisory} advisory")
    if os.getenv("GITHUB_STEP_SUMMARY"):
        # Escaped preformatted JSON prevents findings from injecting Markdown/HTML.
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as summary:
            summary.write(f"## {label}\n\n{blocking} blocking; {advisory} advisory.\n\n")
            summary.write("<pre>" + html.escape(json.dumps(review, indent=2)) + "</pre>\n")
    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
