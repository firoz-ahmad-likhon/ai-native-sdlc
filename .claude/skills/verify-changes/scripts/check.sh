#!/usr/bin/env bash
# Runs the test suite for changed projects and prints the diff evidence
# needed for the weakened-test checklist. Exits non-zero on test failure.
set -uo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

overall_status=0

echo "===== git diff --stat ====="
git diff --stat
git diff --cached --stat

echo
echo "===== test file diff (working tree + staged) ====="
git diff -- '**/src/test/**' '**Test*.java'
git diff --cached -- '**/src/test/**' '**Test*.java'

if [ -d "$REPO_ROOT/spring_boot" ]; then
  echo
  echo "===== mvn test (spring_boot) ====="
  if command -v mvn >/dev/null 2>&1; then
    (cd "$REPO_ROOT/spring_boot" && mvn -q -B test)
    status=$?
    if [ $status -ne 0 ]; then
      echo "mvn test FAILED (exit $status)"
      overall_status=1
    else
      echo "mvn test PASSED"
    fi
  else
    echo "mvn not found on PATH; falling back to Docker build+run"
    (cd "$REPO_ROOT/spring_boot" && docker compose up --build -d)
    status=$?
    if [ $status -ne 0 ]; then
      echo "docker compose up FAILED (exit $status)"
      overall_status=1
    else
      echo "docker compose up succeeded (note: this builds/runs the app, it does not run the JUnit suite)"
    fi
  fi
fi

exit $overall_status
