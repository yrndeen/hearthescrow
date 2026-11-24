#!/usr/bin/env bash
# Public read-only demo of the live Onyx realm + local tests. No keys, no broadcasts.
set -euo pipefail
cd /workspace/bounties/hearthescrow
export PATH="$HOME/go/bin:$HOME/.local/bin:$PATH"
REMOTE="https://rpc.onyx.testnets.gno.land:443"
PKG="gno.land/r/g1x7ud67jym95qh9zf0swmq6ck07s3ly3lksxc5n/hearthescrow"

cap() { printf '\033]1337;PBCAP=%s\007' "$1"; }
run() {
  printf '\033[1;32m$\033[0m \033[1m%s\033[0m\n' "$1"
  sleep 0.5
  eval "$2"
  sleep "${PAUSE:-2.2}"
}
qrender() {
  local path="$1"
  gnokey query vm/qrender -data "${PKG}:${path}" -remote "$REMOTE" \
    | python3 -c 'import sys,re; t=sys.stdin.read(); t=re.sub(r"^height:.*\n","",t); t=re.sub(r"^data: ","",t,count=1); print(t.rstrip())'
}

clear
cap 4
PAUSE=2.5 run "gnokey query vm/qpkgmeta_json -data \"$PKG\" -remote $REMOTE" \
  "gnokey query vm/qpkgmeta_json -data \"$PKG\" -remote \"$REMOTE\""

clear
cap 5
PAUSE=3.5 run "gnokey query vm/qrender … Render(\"\")" "qrender ''"

clear
PAUSE=3.2 run "gnokey query vm/qrender … escrow/1 (COMPLETED)" "qrender 'escrow/1'"

clear
PAUSE=3.2 run "gnokey query vm/qrender … escrow/2 (REFUNDED)" "qrender 'escrow/2'"

clear
cap 6
PAUSE=3.0 run "gno test -v -root-dir /workspace/tools/gno-src ." \
  "gno test -v -root-dir /workspace/tools/gno-src ."
