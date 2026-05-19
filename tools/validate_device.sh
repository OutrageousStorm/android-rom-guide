#!/bin/bash
# validate_device.sh - Check device readiness before ROM flash
# Usage: ./validate_device.sh [device_model]

set -e

DEVICE="${1:-}"

echo -e "\n🔍 Device Pre-Flash Validator"
echo "=============================="

# Check ADB
if ! command -v adb &>/dev/null; then
    echo "❌ ADB not found in PATH"
    exit 1
fi

# Check device connected
if ! adb devices | grep -q "device$"; then
    echo "❌ No device connected (enable USB debugging)"
    exit 1
fi

MODEL=$(adb shell getprop ro.product.model 2>/dev/null)
ANDROID=$(adb shell getprop ro.build.version.release 2>/dev/null)
echo -e "✅ Device connected: ${MODEL} (Android ${ANDROID})"

# Check bootloader status
BL=$(adb shell getprop ro.boot.verifiedbootstate 2>/dev/null)
echo -e "  Bootloader: ${BL:-unknown}"
if [[ "$BL" == "green" ]]; then
    echo -e "  ⚠️  Bootloader is LOCKED (need to unlock first)"
fi

# Check recovery
RECOVERY=$(adb shell getprop ro.recovery_mount_options 2>/dev/null)
[[ -n "$RECOVERY" ]] && echo -e "  ✅ Recovery available"

# Check free storage
STORAGE=$(adb shell df /data | tail -1 | awk '{print $4}')
echo -e "  Free /data: ${STORAGE}KB"
if [[ ${STORAGE:-0} -lt 2097152 ]]; then
    echo -e "  ⚠️  Less than 2GB free (may cause flashing issues)"
fi

# Check battery
BATT=$(adb shell dumpsys battery | grep level | awk '{print $2}')
echo -e "  Battery: ${BATT}%"
if [[ ${BATT:-0} -lt 50 ]]; then
    echo -e "  ⚠️  Battery below 50% (plug in before flashing)"
fi

echo -e "\n✅ Pre-flight checks complete!"
echo "Next: adb reboot bootloader"
