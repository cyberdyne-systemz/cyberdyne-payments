#!/usr/bin/env python3
"""Informational Codex SessionStart hook; no subprocesses or workspace writes."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    event = json.load(sys.stdin)
    if event.get("hook_event_name") != "SessionStart":
        return
    manifest = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
    context = (
        f"Cyberdyne coding-policy {manifest['version']} is loaded. "
        "Read the applicable repository AGENTS.md before editing. "
        "Use the policy MCP tools for shared workflow guidance and prepare-pr for PR work. "
        "Report real test results and cite the source of any policy refusal. "
        "This hook only supplies context; branch protection and required checks enforce Git workflow."
    )
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "SessionStart", "additionalContext": context
    }}))


if __name__ == "__main__":
    main()
