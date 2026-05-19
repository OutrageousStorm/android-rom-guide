#!/bin/bash
# kernel_module_installer.sh -- Install custom kernel modules on rooted Android
# Usage: ./kernel_module_installer.sh module.ko [target_path]
set -e

MODULE="${1:?Usage: $0 <module.ko> [target_path]}"
TARGET="${2:-/vendor/lib/modules}"

[[ ! -f "$MODULE" ]] && echo "❌ Module not found: $MODULE" && exit 1

echo "📦 Kernel Module Installer"
echo "Module: $MODULE"
echo "Target: $TARGET"
echo ""

# Push to device
echo "Pushing to device..."
adb push "$MODULE" /data/local/tmp/
REMOTE_PATH="/data/local/tmp/$(basename "$MODULE")"

# Check architecture
ARCH=$(adb shell uname -m)
echo "Device arch: $ARCH"

# Insert module
echo "Inserting module..."
result=$(adb shell su -c "insmod $REMOTE_PATH" 2>&1)
if [[ $? -eq 0 ]]; then
    echo "✅ Module loaded"
    echo "Listing loaded modules:"
    adb shell lsmod | grep "$(basename "$MODULE" .ko)"
else
    echo "❌ Failed to load: $result"
    exit 1
fi

# Optional: copy to permanent location
read -rp "Copy to $TARGET for persistence? (y/N): " choice
if [[ "$choice" == "y" ]]; then
    adb shell su -c "cp $REMOTE_PATH $TARGET/"
    echo "✅ Copied to $TARGET"
fi

# Cleanup
adb shell rm "$REMOTE_PATH"
echo "✅ Done"
