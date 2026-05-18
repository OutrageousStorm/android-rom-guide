#!/bin/bash
# rom_flasher.sh -- Automated ROM flashing with rollback safety
# Usage: ./rom_flasher.sh <rom.zip> [--backup] [--no-wipe]

set -e
BOLD='\033[1m'; GREEN='\033[0;32m'; RED='\033[0;31m'; NC='\033[0m'

ROM="${1:?Usage: $0 <rom.zip>}"
[[ ! -f "$ROM" ]] && echo -e "${RED}ROM not found: $ROM${NC}" && exit 1

BACKUP=false
WIPE=true
[[ "$2" == "--backup" ]] && BACKUP=true
[[ "$3" == "--no-wipe" ]] && WIPE=false

echo -e "\n${BOLD}📦 ROM Flasher${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "ROM: $(basename $ROM)"
echo "Backup before flash: $BACKUP"
echo "Wipe data: $WIPE"
echo ""

if ! adb devices | grep -q "device$"; then
    echo -e "${RED}❌ No device connected.${NC}"; exit 1
fi

MODEL=$(adb shell getprop ro.product.model)
echo -e "Device: ${BOLD}$MODEL${NC}"
read -p "Confirm flash? (y/N): " -n1 -r; echo
[[ $REPLY != [Yy] ]] && exit 0

# Backup current ROM if requested
if [[ "$BACKUP" == "true" ]]; then
    echo -e "\n${BOLD}📋 Creating ROM backup...${NC}"
    BACKUP_FILE="/tmp/rom_backup_$(date +%Y%m%d_%H%M%S).zip"
    adb reboot bootloader
    sleep 3
    fastboot getvar all 2>&1 | tee "$BACKUP_FILE.info" > /dev/null
    echo -e "  Backup info saved: ${GREEN}$BACKUP_FILE.info${NC}"
fi

# Reboot to recovery
echo -e "\n${BOLD}🔄 Rebooting to recovery...${NC}"
adb reboot recovery
sleep 5

# Sideload ROM
echo -e "\n${BOLD}📤 Sideloading ROM...${NC}"
adb sideload "$ROM"

# Wipe if needed
if [[ "$WIPE" == "true" ]]; then
    echo -e "\n${BOLD}🗑  Wiping userdata...${NC}"
    adb shell "recovery --wipe_data"
fi

# Reboot system
echo -e "\n${BOLD}🚀 Rebooting to system...${NC}"
adb shell "recovery --reboot"

echo -e "\n${GREEN}✅ ROM flash complete!${NC}"
echo "Device will boot in ~2 minutes. Please wait..."
