---
name: multi-module-changes
description: Plan and implement a Cyberdyne change spanning multiple modules or services, preserving repository contracts and testing the affected boundaries. Use for cross-module refactors, shared API changes, or changes with multiple consumers.
---

# Change multiple modules

Read the nearest applicable AGENTS.md in every affected module and the shared workflow from `get_policy(topic="workflow")` (fallback: `../../policy/workflow.md`). Inspect callers, contract types, and tests before choosing scope.

Map the producer, consumers, affected contract, and verification command for each boundary. Explain this map briefly before editing. If a contract change could break a consumer, resolve compatibility explicitly and prefer a staged migration where needed.

Implement one coherent change at a time. Keep unrelated cleanup out. Run narrow module tests, then the relevant integration or repository check. Report skipped boundaries and their consequences. Cite conflicting repository instructions instead of silently choosing one.

Use the `prepare-pr` skill to package the completed change when requested. Do not split or publish multiple PRs without a task need and user authorization.
