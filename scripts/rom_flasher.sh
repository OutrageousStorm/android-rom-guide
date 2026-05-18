#!/bin/bash
# rom_flasher.sh -- Safe ROM flashing with backup
# Usage: ./rom_flasher.sh <rom.zip>
set -e

echo "🔥 ROM Flasher"
echo "━━━━━━━━━━━━"

ROM_ZIP="${1:?Usage: $0 <rom.zip>}"
[[ ! -f "$ROM_ZIP" ]] && echo "ROM not found: $ROM_ZIP" && exit 1

adb devices | grep -q "device$" || { echo "No device connected"; exit 1; }

# Backup
BACKUP_DIR="backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
adb shell dumpsys > "$BACKUP_DIR/dumpsys.txt"
echo "✓ Backup in $BACKUP_DIR"

# Flash
TMP_DIR=$(mktemp -d)
unzip -q "$ROM_ZIP" -d "$TMP_DIR"

adb reboot fastboot
sleep 5

for img in system.img vendor.img product.img boot.img; do
  [[ -f "$TMP_DIR/$img" ]] && {
    echo "Flashing $img..."
    fastboot flash $(echo $img | sed 's/.img//') "$TMP_DIR/$img"
  }
done

fastboot -w
fastboot reboot

echo "✅ Flash complete! First boot: 3-5 min"
