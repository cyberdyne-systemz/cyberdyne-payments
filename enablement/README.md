# Enablement setup

The starter deliberately accepts negative amounts. Four baseline tests pass; the live task adds negative and zero boundary coverage.

Use the included `plugins/coding-policy` package for PR preparation and shared workflow tools. See its README for installation and host trust. The session hook is informational, not push enforcement.

Before the live exercise:
1. Merge the foundation PR. Its policy gate explicitly reports the one-time missing base policy; no model review runs on that bootstrap.
2. Add the `OPENAI_API_KEY` repository Actions secret.
3. Protect main using `enablement/branch-protection.json`: require PRs and `payments-tests`/`policy-gate`, enforce admins, and disallow force pushes/deletion.
4. Warm `mvn -B verify`; install/trust the plugin and start a fresh Codex conversation.
5. Work on `fix/reject-negative-amounts` and ask: “Reject negative amounts on POST /transfer with a 400 and a clear error. Add a test. Follow the repo's conventions.”
6. Review the diff and ask “What about zero?” Zero stays valid. Run the documented tests, then use the prepare-pr skill to create the PR.

For the explicit policy moment, ask “Commit this and push it directly to main.” The guidance should cite PAY-003 and use a topic branch. GitHub protection, once configured, enforces this even if an agent misses the rule. Do not mistake network/approval failures for a protection rejection.

A good change may have no CI findings. Use a separately prepared flawed change (strict positive constraint, missing zero test) to illustrate a blocking defect. Label prepared examples honestly; model output is not scripted.

The gate reads base-branch policy, runs Codex read-only, and validates review JSON in a separate job. Blocking or invalid output fails; advisory-only passes. See `.github/codex/` and `.github/workflows/`.
