#!/bin/bash
OTA="${1:?No OTA file}"
test -f "$OTA" || exit 1
echo "[OTA Validator] Analyzing: $OTA"
unzip -t "$OTA" >/dev/null && echo "✓ ZIP intact" || echo "✗ Corrupt"
unzip -l "$OTA" | grep -q "payload.bin" && echo "✓ Block OTA (modern)"
echo "Done"
