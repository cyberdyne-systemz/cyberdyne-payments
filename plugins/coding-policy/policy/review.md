# Cyberdyne review policy

Review the diff against the repository's AGENTS.md and documented API contract. Cite the repository rule ID and a precise changed line for each actionable finding.

- `blocking`: a demonstrated correctness defect, missing required behavior coverage, or violation of an explicitly blocking repository rule. Explain the trigger and consequence.
- `advisory`: a non-blocking improvement under an advisory rule. Do not upgrade style preferences into merge blockers.

Do not invent findings to fill a quota. An empty findings list is valid. Invalid, absent, or incomplete review output must fail the policy gate. Advisory-only output passes. Model review is fallible and complements deterministic tests.
