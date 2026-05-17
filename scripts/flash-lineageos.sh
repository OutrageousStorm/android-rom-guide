#!/bin/bash
# flash-lineageos.sh -- Auto-detect device and flash LineageOS
# Usage: ./flash-lineageos.sh <device-codename>
# Example: ./flash-lineageos.sh panther  (Pixel 7)

set -e

CODENAME="${1:?Usage: $0 <device_codename>}"
DEVICE_REPO="https://raw.githubusercontent.com/LineageOS/hudson/main"

echo "🤖 LineageOS Auto-Flasher"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Device: $CODENAME"

# Check for prerequisites
for tool in adb fastboot curl wget; do
    if ! command -v $tool &> /dev/null; then
        echo "❌ Missing: $tool"
        exit 1
    fi
done

# Get device info
DEVICE_JSON=$(curl -s "$DEVICE_REPO/devices.json" | grep -A5 "\"$CODENAME\"" | head -20)
if [[ -z "$DEVICE_JSON" ]]; then
    echo "❌ Device not found: $CODENAME"
    exit 1
fi

echo "✓ Device found in LineageOS database"

# Detect current ROM and version
MODEL=$(adb shell getprop ro.product.model)
ANDROID=$(adb shell getprop ro.build.version.release)
echo "  Current: $MODEL (Android $ANDROID)"

# Download latest LineageOS for this device
BUILD_URL="https://download.lineageos.org/devices/$CODENAME"
echo "  Downloading LineageOS..."
curl -s -L "$BUILD_URL" | grep -oP '(?<=href=")[^"]*\.zip(?=")' | head -1 > /tmp/lineage_url.txt
LINEAGE_ZIP=$(cat /tmp/lineage_url.txt)

if [[ -z "$LINEAGE_ZIP" ]]; then
    echo "❌ Could not find LineageOS build"
    exit 1
fi

echo "  URL: $LINEAGE_ZIP"

# Boot to recovery
echo "📱 Rebooting to recovery..."
adb reboot recovery
sleep 10

# Flash via ADB sideload (safest method)
echo "💾 Sideloading LineageOS..."
adb sideload "$LINEAGE_ZIP"

# Optional: Flash GApps
read -p "Install GApps (Y/n)? " -n1 GAPPS
[[ "$GAPPS" != "n" ]] && echo "💾 Flash GApps in recovery: Settings → Wipe → Flash additional OTAs"

echo ""
echo "✅ Done! Device will reboot."
echo "   First boot may take 2-3 minutes."
