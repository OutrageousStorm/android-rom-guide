#!/bin/bash
# recovery-fixer.sh -- Fix common recovery/bootloader issues
# Usage: ./recovery-fixer.sh [issue]
# Issues: recovery-not-found, stuck-bootloop, fastboot-timeout, adb-offline

set -e

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BOLD='\033[1m'; NC='\033[0m'

echo -e "\n${BOLD}🔧 Android Recovery Fixer${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"

case "${1:-menu}" in
  recovery-not-found)
    echo -e "${YELLOW}Recovery not found in boot image${NC}"
    echo "Solutions:"
    echo "  1. Reflash recovery via fastboot"
    adb reboot bootloader 2>/dev/null || echo "  Device not responding via ADB"
    sleep 2
    echo "  Device should now be in fastboot mode..."
    fastboot flash recovery recovery.img
    echo -e "${GREEN}✓ Recovery reflashed${NC}"
    ;;
  stuck-bootloop)
    echo -e "${YELLOW}Device stuck in bootloop${NC}"
    echo "Solution: Force fastbootd mode (hold Power + Vol Down)"
    read -p "  Press Enter when device shows fastboot... "
    echo "  Booting into recovery..."
    fastboot reboot-recovery || fastboot reboot
    ;;
  fastboot-timeout)
    echo -e "${YELLOW}Fastboot connection timing out${NC}"
    echo "Fixes:"
    echo "  • Try: fastboot --set-active=a"
    echo "  • Unplug/replug device"
    echo "  • Try different USB port (not USB 3.0)"
    fastboot devices -l
    ;;
  adb-offline)
    echo -e "${YELLOW}ADB shows offline${NC}"
    echo "Fixing..."
    adb kill-server
    sleep 1
    adb devices
    echo -e "${GREEN}✓ ADB restarted${NC}"
    ;;
  *)
    echo "Issues:"
    echo "  ./recovery-fixer.sh recovery-not-found"
    echo "  ./recovery-fixer.sh stuck-bootloop"
    echo "  ./recovery-fixer.sh fastboot-timeout"
    echo "  ./recovery-fixer.sh adb-offline"
    ;;
esac
