# Coding Policy — Cyberdyne enablement plugin

Version 0.1.0. This is a local Codex plugin for the fictional Cyberdyne training scenario, not a production organizational policy service.

- `prepare-pr`: grounds the PR in the actual diff, repository template, and observed checks.
- `multi-module-changes`: maps producers, consumers, contracts, and verification before editing.
- `hooks/hooks.json`: SessionStart context reminder with the installed version. Users must review/trust the hook in Codex before it runs.
- `cyberdyne-policy` MCP: dependency-free Python 3 stdio server, exposing `get_policy` (`workflow` or `review`) and `get_pr_template`. Reads only bundled files; no credentials, network calls, or writes.

The compatibility manifest is `.codex-plugin/plugin.json`. Install this whole `coding-policy` directory, not the older presentation workspace's root `plugin.json` stub. Python 3 must be on the Codex host's PATH. Start a new conversation after installing or updating.

## Install for a presenter

In Codex, ask the built-in `plugin-creator` skill:

> Add this existing coding-policy plugin to my personal marketplace and install it. Preserve its files and existing marketplace entries.

Provide the absolute path to this folder. That operation updates personal Codex files and is separate from building the package. After installation, review/trust the displayed SessionStart hook. Confirm that the plugin's two skills and two MCP tools appear in a new conversation. Call `get_policy` with `workflow`; it should report `coding-policy 0.1.0` and the source filename. If MCP is unavailable, skills can read the bundled Markdown and must disclose the fallback.

The session hook uses Codex's `PLUGIN_ROOT`. The bundled MCP configuration sets `cwd` to the plugin root and uses a relative script path, so it also works after copying into Codex's plugin cache. The package targets Codex CLI 0.154.0. Host installation/trust still needs an actual smoke test before presenting.

## Verify without installing

From the payments repository: `python3 -m unittest discover -s enablement/tests -v`.

These tests exercise MCP initialization/list/call/error handling, the session hook's JSON output, and the CI gate. They do not claim that a model chose a skill or that a host trusted the hook.

## Ownership and enforcement

Developer Platform maintains `policy/`, skills, and hooks. Repository maintainers own `AGENTS.md`, contracts, and tests. Hooks and skill prose guide behavior. GitHub branch protection and required checks enforce merge gates.

Format references: [build plugins](https://learn.chatgpt.com/docs/build-plugins), [hooks](https://learn.chatgpt.com/docs/hooks), [MCP stdio](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports).
