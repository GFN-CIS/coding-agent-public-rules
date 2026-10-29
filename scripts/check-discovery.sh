#!/usr/bin/env bash
# Deterministic (no-LLM) check that OpenCode discovers the gfn-* skills
# from a `skills: [<repo>]` config entry.
#
# Usage: check-discovery.sh <opencode-binary> [repo-root]
#
# Notes on the mechanism (verified against OpenCode v2.2.1):
# - GET /api/skill returns [] until a location instance exists on the server;
#   creating a session in a directory (POST /api/session, no prompt, no LLM)
#   initialises it, after which the route lists the full skill registry.
# - The registry listing INCLUDES hidden skills (it also lists
#   permission-denied ones), so all 11 gfn-* ids are asserted here.
#   gfn-code-health-check's autoinvoke:false hides it from the model-facing
#   list, not from this registry; that behaviour is covered by the manual
#   `opencode run` verification, not by this script.
set -euo pipefail

OPENCODE_BIN=${1:?usage: check-discovery.sh <opencode-binary> [repo-root]}
REPO_ROOT=$(cd "${2:-$(dirname "$0")/..}" && pwd)
PORT=43999

WORK=$(mktemp -d)
SERVER_PID=""
cleanup() { [ -n "$SERVER_PID" ] && kill "$SERVER_PID" 2>/dev/null || true; rm -rf "$WORK"; }
trap cleanup EXIT

export XDG_CONFIG_HOME="$WORK/config"
export OPENCODE_PASSWORD=ci-discovery
mkdir -p "$XDG_CONFIG_HOME/opencode"
printf '{"skills":["%s"]}' "$REPO_ROOT" > "$XDG_CONFIG_HOME/opencode/opencode.json"

"$OPENCODE_BIN" serve --port "$PORT" > "$WORK/serve.log" 2>&1 &
SERVER_PID=$!

for _ in $(seq 1 30); do
  "$OPENCODE_BIN" api --server "http://127.0.0.1:$PORT" get /api/info > /dev/null 2>&1 && break
  sleep 1
done

# initialise a location instance so GET /api/skill lists skills (see header note)
"$OPENCODE_BIN" api --server "http://127.0.0.1:$PORT" post /api/session \
  -d "{\"location\":{\"directory\":\"$WORK\"}}" > /dev/null

# the skill registry populates lazily after the location boots: retry until it answers
for i in $(seq 1 30); do
  "$OPENCODE_BIN" api --server "http://127.0.0.1:$PORT" skill.list > "$WORK/skills.json" 2>/dev/null || true
  if python3 -c "import json,sys; d=json.load(open(sys.argv[1])); sys.exit(0 if any(s['id'].startswith('gfn-') for s in d['data']) else 1)" "$WORK/skills.json"; then
    break
  fi
  sleep 1
done

python3 - "$WORK/skills.json" <<'PY'
import json
import sys

expected = [
    "gfn-ansible", "gfn-ci-cd", "gfn-code", "gfn-code-health-check",
    "gfn-code-reviewing", "gfn-docker", "gfn-infrastructure", "gfn-kubernetes",
    "gfn-python", "gfn-terraform", "gfn-testing",
]
ids = sorted(s["id"] for s in json.load(open(sys.argv[1]))["data"])
gfn = [i for i in ids if i.startswith("gfn-")]
missing = [i for i in expected if i not in gfn]
extra = [i for i in gfn if i not in expected]
if missing or extra:
    print(f"FAIL: missing={missing} extra={extra} (found {len(gfn)} gfn-* ids)")
    sys.exit(1)
print(f"OK: OpenCode discovered all {len(expected)} gfn-* skills:")
print("  " + ", ".join(gfn))
PY
