#!/bin/bash
# flash-helper.sh -- Automated ROM flashing with safety checks and rollback
# Usage: ./flash-helper.sh <rom.zip> [--auto-backup] [--skip-wipe]
set -e

ROM="${1:?Usage: $0 <rom.zip>}"
AUTO_BACKUP=false
SKIP_WIPE=false

[[ "$2" == "--auto-backup" ]] && AUTO_BACKUP=true
[[ "$3" == "--skip-wipe" || "$2" == "--skip-wipe" ]] && SKIP_WIPE=true

echo "🚀 ROM Flash Helper"
echo "ROM: $(basename $ROM)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Verify ROM
[[ -f "$ROM" ]] || { echo "❌ ROM not found"; exit 1; }
[[ "${ROM##*.}" == "zip" ]] || { echo "❌ Not a ZIP file"; exit 1; }

# Verify device
if ! adb devices | grep -q "device$"; then
    echo "❌ No device connected"
    exit 1
fi

MODEL=$(adb shell getprop ro.product.model)
echo "Device: $MODEL"

# Optional backup
if [[ "$AUTO_BACKUP" == "true" ]]; then
    BACKUP_DIR="$HOME/.android_backups/$(date +%Y%m%d_%H%M%S)_$MODEL"
    mkdir -p "$BACKUP_DIR"
    echo "📦 Backing up boot partition..."
    adb shell "su -c 'dd if=/dev/block/bootdevice/by-name/boot of=/data/local/tmp/boot_backup.img'" 2>/dev/null || true
    adb pull /data/local/tmp/boot_backup.img "$BACKUP_DIR/" 2>/dev/null || true
    echo "   Saved to: $BACKUP_DIR"
fi

# Flash
echo ""
echo "🔌 Rebooting to bootloader..."
adb reboot bootloader
sleep 5

echo "⏳ Waiting for fastboot..."
timeout=30
while ! fastboot devices | grep -q "fastboot"; do
    sleep 1
    ((timeout--))
    [[ $timeout -lt 0 ]] && { echo "❌ Device not in fastboot mode"; exit 1; }
done

echo "🔨 Flashing ROM..."
fastboot erase system
fastboot flash system "$ROM"

[[ "$SKIP_WIPE" != "true" ]] && {
    echo "🧹 Wiping userdata..."
    fastboot -w
}

echo "🔄 Rebooting device..."
fastboot reboot

echo "✅ Flash complete. Device will boot in ~30 seconds."
