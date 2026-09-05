# Weakened-Test Checklist

A test suite going green after a change is not by itself evidence the change is correct — the tests could have been loosened to fit whatever the code now does, rather than the code being fixed to satisfy the tests. Check the diff of every changed test file against each item below before reporting a pass.

- **Assertion removed.** A line asserting a specific outcome (`assertEquals`, `andExpect`, etc.) was deleted rather than kept and made to pass honestly.
- **Assertion loosened.** An exact-match check became a substring/contains check, a strict equality became a range or tolerance, or a specific expected value was replaced with a wildcard/any-matcher.
- **Test disabled or skipped.** `@Disabled`, `@Ignore`, `@Test(enabled = false)`, or the test body/annotation commented out, without a linked tracking issue explaining why.
- **Test deleted.** A test method or class removed entirely instead of updated to reflect intended new behavior.
- **Expected value changed to match new behavior, not intended behavior.** The expected status code, return value, or exception type in the test was edited to match whatever the changed code now happens to produce, rather than the change being verified against the behavior the task actually called for.
- **Reduced input coverage.** A parameterized or table-driven test had cases removed, and the removed case happens to be the one that would have failed.
- **Exception swallowing.** A `try/catch` was added around an assertion that silently absorbs a failure instead of letting it propagate.

If any of these apply, the check fails even if the test run reports green — say so explicitly and point to the diff hunk that shows it.
