#!/bin/bash
# bulk_install_apks.sh -- Install multiple APKs from a directory via ADB
# Usage: ./bulk_install_apks.sh /path/to/apk/folder

set -e
APK_DIR="${1:-.}"
[[ ! -d "$APK_DIR" ]] && echo "Directory not found: $APK_DIR" && exit 1

echo "📦 Installing APKs from $APK_DIR"
installed=0; failed=0
for apk in "$APK_DIR"/*.apk; do
    [[ -f "$apk" ]] || continue
    name=$(basename "$apk")
    if adb install -r -g "$apk" > /dev/null 2>&1; then
        echo "  ✓ $name"
        ((installed++))
    else
        echo "  ✗ $name"
        ((failed++))
    fi
done
echo "Installed: $installed  Failed: $failed"
