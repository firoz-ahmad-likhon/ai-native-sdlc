---
name: verify-changes
description: Use this after completing a code change (a refactor, bug fix, or feature) and before declaring it done. Runs the project's test suite, reviews the diff, and checks that no test assertion was weakened just to make things pass. Applies to changes in spring_boot/ and any future project this repo's intent/design/plan loop produces.
---

# Verify Changes

Don't call a change done because the code "looks right." Done means the gates were actually run and their results are stated explicitly, with evidence.

1. Run `scripts/check.sh` from the repo root. It runs the test suite and captures the diff — execute it, don't read its source into context.
2. Read the diff of any test files it reports as changed.
3. Check that diff against the weakened-test checklist in `reference.md`.
4. Report explicitly:
   - The exact command that ran and its pass/fail result (quote the test summary line).
   - Whether any test was weakened, and if so, which check from `reference.md` it tripped, with the diff hunk as evidence.
   - If `check.sh` failed outright, stop and fix the underlying issue — do not report success anyway.
