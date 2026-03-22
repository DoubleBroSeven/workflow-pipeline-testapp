#!/usr/bin/env bash
set -euo pipefail

# Local CI — mirrors the GitHub Actions CI pipeline
echo "=== Local CI ==="

FAILED=()

echo "--- Build ---"
if echo "No build command configured"; then
  echo "Build: PASS"
else
  FAILED+=("build")
  echo "Build: FAIL"
fi

echo "--- Tests ---"
if pytest; then
  echo "Tests: PASS"
else
  FAILED+=("tests")
  echo "Tests: FAIL"
fi

echo ""
if [ ${#FAILED[@]} -eq 0 ]; then
  echo "All checks passed."
  exit 0
else
  echo "FAILED: ${FAILED[*]}"
  exit 1
fi
