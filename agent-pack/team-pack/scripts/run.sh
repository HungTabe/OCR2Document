#!/usr/bin/env bash
# Run the exam-prep pipeline headless.
#   scripts/run.sh [--input DIR] [--exam NAME] [--profile ccdvp] [--mode full|quick] [--from N] [--to N] [--modules reuse|build]
# The orchestrator must be the MAIN agent (sub-agents cannot spawn sub-agents), so we start it with --agent.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
INPUT="$ROOT/agent-pack/team-pack/input"; EXAM="de"; PROFILE="ccdvp"; MODE="full"; FROM="1"; TO="10"; MODULES="reuse"
while [ $# -gt 0 ]; do
  case "$1" in
    --input) INPUT="$(cd "$2" && pwd)"; shift 2;;
    --exam) EXAM="$2"; shift 2;;
    --profile) PROFILE="$2"; shift 2;;
    --mode) MODE="$2"; shift 2;;
    --from) FROM="$2"; shift 2;;
    --to) TO="$2"; shift 2;;
    --modules) MODULES="$2"; shift 2;;
    -h|--help) sed -n '2,5p' "$0"; exit 0;;
    *) echo "unknown option: $1" >&2; exit 2;;
  esac
done
cd "$ROOT"
TOOLS=(Agent Read Write Glob "Bash(python3 *)" "Bash(node *)" "Bash(ls *)" "Bash(wc *)" "Bash(mkdir *)" "Bash(mv *)" "Bash(cp *)" "Bash(cat *)" "Bash(test *)" "Bash(date *)" "Bash(pwd)")
if [ "$MODULES" = "build" ]; then TOOLS+=(WebSearch WebFetch); fi
exec claude --agent exam-orchestrator -p \
  "Run the pipeline. INPUT=$INPUT EXAM=$EXAM PROFILE=$PROFILE MODE=$MODE FROM=$FROM TO=$TO MODULES=$MODULES" \
  --permission-mode acceptEdits --allowedTools "${TOOLS[@]}"
