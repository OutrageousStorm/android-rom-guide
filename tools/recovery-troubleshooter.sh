#!/bin/bash
# Recovery Troubleshooter
# Diagnose and fix common recovery/flashing issues

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔧 Recovery Troubleshooter${NC}\n"

# Check fastboot connection
echo -e "${YELLOW}1. Checking fastboot connection...${NC}"
if fastboot devices | grep -q '.*	'; then
    echo -e "${GREEN}✅ Device detected in fastboot mode${NC}"
else
    echo -e "${RED}❌ No device in fastboot mode${NC}"
    echo "   → Reconnect device in bootloader mode"
    echo "   → On most phones: Power off, then hold Volume Down + Power"
    exit 1
fi

# Check device bootloader
echo -e "\n${YELLOW}2. Checking bootloader state...${NC}"
BOOTLOADER=$(fastboot getvar bootloader 2>&1 | grep bootloader | cut -d' ' -f2)
echo "   Bootloader: $BOOTLOADER"

# Check device tree
echo -e "\n${YELLOW}3. Checking recovery partition...${NC}"
RECOVERY=$(fastboot getvar recovery-size 2>&1 | grep recovery | cut -d' ' -f2)
if [ -z "$RECOVERY" ]; then
    echo -e "${YELLOW}⚠️  Recovery partition info unavailable${NC}"
else
    echo -e "${GREEN}✅ Recovery partition detected${NC}"
fi

# Common fixes
echo -e "\n${YELLOW}4. Common Recovery Issues:${NC}"

echo ""
echo -e "${YELLOW}Issue: Boot loop after flash${NC}"
echo "   Fix: Boot into recovery and factory reset"
echo "   $ fastboot boot recovery.img"

echo ""
echo -e "${YELLOW}Issue: Cannot enter bootloader${NC}"
echo "   Fix: Try ADB reboot bootloader (if ADB works)"
echo "   $ adb reboot bootloader"

echo ""
echo -e "${YELLOW}Issue: Fastboot not found${NC}"
echo "   Fix: Install Android SDK Platform Tools"
echo "   $ brew install android-platform-tools  # macOS"
echo "   $ sudo apt install android-tools-fastboot  # Linux"

echo -e "\n${GREEN}✅ Troubleshooter complete${NC}"
