#!/bin/bash
# Android ROM Flashing Helper — Pre-flash checks, bootloader detection, device validation
# For use with LineageOS, GrapheneOS, CalyxOS, crDroid, and other custom ROMs

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}ℹ️${NC} $1"; }
log_success() { echo -e "${GREEN}✅${NC} $1"; }
log_warn() { echo -e "${YELLOW}⚠️${NC} $1"; }
log_error() { echo -e "${RED}❌${NC} $1"; }

check_adb() {
    if ! command -v adb &> /dev/null; then
        log_error "ADB not found. Install Android SDK Platform Tools."
        exit 1
    fi
    log_success "ADB found"
}

check_fastboot() {
    if ! command -v fastboot &> /dev/null; then
        log_error "Fastboot not found. Install Android SDK Platform Tools."
        exit 1
    fi
    log_success "Fastboot found"
}

get_devices() {
    local devices=$(adb devices | grep -v "^List" | grep -v "^$" | awk '{print $1}' | grep -v "device$")
    echo "$devices"
}

check_device_connected() {
    local devices=$(get_devices)
    if [ -z "$devices" ]; then
        log_error "No devices connected via ADB. Enable USB debugging."
        exit 1
    fi
    log_success "Device(s) connected: $devices"
}

get_device_info() {
    local device=$1
    log_info "Device information:"
    adb -s "$device" shell getprop ro.build.product
    adb -s "$device" shell getprop ro.build.version.release
    adb -s "$device" shell getprop ro.build.fingerprint
}

check_bootloader_unlock() {
    local device=$1
    log_info "Checking bootloader status..."
    
    # Reboot to bootloader
    adb -s "$device" reboot bootloader
    sleep 3
    
    local unlock_status=$(fastboot getvar unlocked 2>&1 || echo "unknown")
    
    if [[ "$unlock_status" == *"yes"* ]]; then
        log_success "Bootloader is UNLOCKED ✓"
    elif [[ "$unlock_status" == *"no"* ]]; then
        log_warn "Bootloader is LOCKED"
        log_info "Unlock bootloader:"
        log_info "  1. Connect device in fastboot mode"
        log_info "  2. Run: fastboot flashing unlock"
        log_info "  3. Confirm on device"
        return 1
    else
        log_warn "Could not determine bootloader status"
    fi
    
    # Reboot back to system
    fastboot reboot
    sleep 3
    log_success "Device rebooted"
}

validate_rom_file() {
    local rom_file=$1
    
    if [ ! -f "$rom_file" ]; then
        log_error "ROM file not found: $rom_file"
        return 1
    fi
    
    log_success "ROM file found: $(basename $rom_file)"
    log_info "File size: $(du -h "$rom_file" | cut -f1)"
    
    # Check if ZIP
    if file "$rom_file" | grep -q ZIP; then
        log_success "Valid ZIP archive"
    else
        log_warn "File may not be a valid ZIP"
    fi
}

show_usage() {
    cat << USAGE
Android ROM Flashing Helper

Usage: $0 [options]

Options:
  --check-all           Run all pre-flash checks
  --device SERIAL       Target device serial
  --rom FILE            Validate ROM file
  --unlock              Check & guide bootloader unlock
  
Examples:
  $0 --check-all --device emulator-5554
  $0 --unlock --device RF8M30C9JTJ
  $0 --rom LineageOS-21-20240523-hammerhead.zip

USAGE
}

# Main
main() {
    check_adb
    check_fastboot
    
    local device=""
    local rom_file=""
    local check_all=false
    local unlock=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --check-all) check_all=true; shift ;;
            --device) device="$2"; shift 2 ;;
            --rom) rom_file="$2"; shift 2 ;;
            --unlock) unlock=true; shift ;;
            --help) show_usage; exit 0 ;;
            *) log_error "Unknown option: $1"; show_usage; exit 1 ;;
        esac
    done
    
    if [ -z "$device" ]; then
        check_device_connected
        local devices=$(get_devices)
        device=$(echo "$devices" | head -1)
        log_info "Using device: $device"
    fi
    
    if [ "$check_all" = true ]; then
        get_device_info "$device"
        check_bootloader_unlock "$device"
        log_success "Pre-flash checks complete!"
    fi
    
    if [ -n "$rom_file" ]; then
        validate_rom_file "$rom_file"
    fi
    
    if [ "$unlock" = true ]; then
        check_bootloader_unlock "$device"
    fi
}

main "$@"
