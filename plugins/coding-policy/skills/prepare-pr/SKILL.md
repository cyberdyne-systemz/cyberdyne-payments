---
name: prepare-pr
description: Prepare or create a Cyberdyne pull request from the current diff using repository policy, the PR template, and real verification evidence. Use when asked to prepare a PR, describe a change for review, or commit and publish a completed change.
---

# Prepare a Cyberdyne PR

1. Read applicable `AGENTS.md` and `.github/pull_request_template.md`. Call the bundled `get_policy` tool with topic `workflow`; fall back to `../../policy/workflow.md` if MCP is unavailable and disclose the fallback. The repository owns domain rules.
2. Inspect `git status --short`, current branch, remotes, and the actual base-to-head diff. Detect the default branch from the remote instead of assuming its name. Account for uncommitted work. Never stage unrelated edits.
3. Follow repository branch rules. If on the protected branch, cite the exact rule and create the authorized topic branch before committing. Do not bypass protection or force push. Report approval or network failures as such, not as policy rejections.
4. Run the repository's narrow check and required pre-PR checks when feasible. Record actual outcomes. If a command cannot run, state why and keep the check unverified. Review boundary behavior, API compatibility, and error messages in the diff.
5. Write a short title (`fix(payments): reject negative transfer amounts`) and fill the repository template from the diff. If no template exists, call `get_pr_template` or read `../../policy/pr-template.md`. Include rule IDs, exact checks, and any limits.
6. For a preparation-only request, write the draft to an ignored local file and return its path. When the user asks to publish/create a PR, commit only the intended files, push the topic branch, and use `gh pr create --body-file <file>` (or update an existing PR). Do not add a redundant approval step within already authorized scope. If no GitHub remote or authentication exists, provide the ready draft and explain the specific missing input. Do not claim the local draft is a GitHub PR.
7. Return the actual PR URL when created, checks observed so far, and remaining work. Do not merge unless requested.
