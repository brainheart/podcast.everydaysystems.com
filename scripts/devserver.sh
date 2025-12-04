#!/usr/bin/env bash
set -euo pipefail

# Simple dev server launcher for the podcast site.
# - Picks a free port (prefers common ports, then falls back to an ephemeral one)
# - Starts python http.server bound to 127.0.0.1
# - Writes PID to .devserver.pid in repo root
# - Tries to open the browser to the main index

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

choose_port() {
  local candidates=(8081 8082 8888 5500 5173 3000)
  local p
  if command -v lsof >/dev/null 2>&1; then
    for p in "${candidates[@]}"; do
      if ! lsof -nP -iTCP -sTCP:LISTEN | grep -q ":$p\b"; then
        echo "$p"
        return 0
      fi
    done
  fi
  # Fallback: ask Python for a free ephemeral port
  python3 - "$@" << 'PY'
import socket
s = socket.socket()
s.bind(("127.0.0.1", 0))
port = s.getsockname()[1]
s.close()
print(port)
PY
}

PORT="${1:-}"
if [[ -z "${PORT}" ]]; then
  PORT=$(choose_port)
fi

# Stop any prior server started via this script
if [[ -f .devserver.pid ]]; then
  if kill -0 "$(cat .devserver.pid)" 2>/dev/null; then
    echo "Stopping previous server PID $(cat .devserver.pid)"
    kill "$(cat .devserver.pid)" || true
    # Give it a moment
    sleep 0.3 || true
  fi
  rm -f .devserver.pid
fi

echo "Starting dev server on http://localhost:${PORT}/"
nohup python3 -m http.server --bind 127.0.0.1 "${PORT}" >/dev/null 2>&1 &
echo $! > .devserver.pid
echo "Server PID $(cat .devserver.pid)"

# Try to open the browser
URL="http://localhost:${PORT}/"
if command -v open >/dev/null 2>&1; then
  open "$URL" || true
elif command -v xdg-open >/dev/null 2>&1; then
  xdg-open "$URL" || true
else
  echo "Open your browser to: $URL"
fi

echo "Tip: stop with 'kill \$(cat .devserver.pid)' from the repo root."

