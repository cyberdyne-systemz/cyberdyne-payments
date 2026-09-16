# Cyberdyne shared workflow

Owner: Developer Platform. Repository maintainers own their AGENTS.md and domain contracts.

1. Ground the change in the applicable AGENTS.md, nearby implementation, and tests. Resolve scope and contract ambiguity before changing behavior.
2. Use a topic branch. Inspect the current branch and worktree before committing. Preserve the user's changes. Repository branch protection is the enforcement boundary.
3. Make the smallest coherent change, inspect its diff, and verify the behavior and relevant boundaries. Report exact commands and results; label checks that were not run.
4. Prepare a PR from the actual base-to-head diff and repository PR template. Use a title such as `fix(payments): reject negative transfer amounts`. Document risks and remaining checks.
5. Publish a branch or PR when the user requests that action. Never invent a PR URL or CI result. A prepared review fixture must be identified as prepared.

Skills and hooks provide workflow guidance. They do not replace sandbox permissions, server-side branch protection, required CI checks, or human review.
