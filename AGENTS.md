# Cyberdyne Payments repository conventions

Owner: Payments maintainers. Shared workflow owner: Developer Platform (`coding-policy`).

## Grounding

Read `docs/api.md`, the request DTO, controller, exception handler, and nearby tests before changing validation. Use Java 21 and Maven. Keep the change scoped to the task.

## PAY-001 — API contract (blocking)

`POST /transfer` accepts amounts greater than or equal to zero. Zero is a supported no-op in this demo. Negative amounts return HTTP 400 with `VALIDATION_ERROR` and a client-actionable field error. Use `BigDecimal`, never floating point, for amounts. The service is an in-memory teaching stub and does not move money.

## PAY-002 — Validation and tests (blocking)

Use Jakarta Bean Validation on request records and the existing `ApiExceptionHandler` error envelope. Do not add a second validation/error path in the controller. Every behavior change needs an HTTP-level regression test. For amount validation cover a negative decimal, zero, and a positive amount; keep missing-amount behavior intact.

Run the narrowest relevant test first: `mvn -B -Dtest=TransferControllerTest test`. Run `mvn -B verify` before proposing a merge. Report actual commands and outcomes; never turn an unrun check into a passing claim.

## PAY-003 — Git workflow (blocking)

Work on `fix/<short-topic>` or `feat/<short-topic>`. Never commit or push directly to `main`; create a topic branch first. Do not force push. When a request conflicts with this rule, cite `AGENTS.md → PAY-003` and continue with the branch/PR workflow already authorized by the task. Preserve existing work.

## PAY-004 — Pull requests

Use `.github/pull_request_template.md`. Describe the actual diff, exact validation evidence, and remaining limits. Developer Platform's `prepare-pr` skill packages this workflow. Commit/push/create a PR only within the user's requested scope.

## PAY-005 — Documentation (advisory)

When changing validation, add a concise request/error example in `docs/api.md`. Missing examples are advisory unless the documented behavior contradicts the contract, which is PAY-001.

## Enforcement

This file guides agents and reviewers. GitHub branch protection and required `payments-tests` and `policy-gate` checks enforce the merge workflow. A hook reminder is not branch protection. A model review may miss a defect; tests and human review remain necessary.
