# ROM Flashing Troubleshooting

Common issues and solutions when flashing custom ROMs.

## Boot Loops

**Issue:** Device stuck on boot animation or logo screen

**Causes:**
- Incompatible ROM for your device
- Incomplete wipe (didn't wipe /data or /cache)
- Corrupted system partition

**Fix:**
1. Boot to recovery
2. Wipe Dalvik/ART Cache + Cache + Data
3. Flash ROM again
4. If still broken, restore backup from TWRP

## ForceClose Errors on First Boot

**Issue:** Apps crashing with "Unfortunately X has stopped"

**Causes:**
- ROM didn't finish optimizing on first boot
- Missing GApps
- Incompatible Magisk module

**Fix:**
1. Let device sit for 5–10 minutes (optimizing apps)
2. Reboot
3. Check logcat: `adb logcat | grep FATAL`

## No Mobile Signal / Call Issues

**Issue:** Device won't connect to cellular network

**Causes:**
- Modem partition not flashed
- Device tree mismatch
- Firmware mismatch

**Fix:**
```bash
# Re-flash modem (requires original firmware)
adb reboot bootloader
fastboot flash modem modem.img
fastboot reboot
```

## Can't Mount Internal Storage

**Issue:** /data partition won't mount in recovery

**Causes:**
- Encryption mismatch
- Corrupted partition table

**Fix:**
```bash
# In TWRP: Advanced → ADB Sideload
adb sideload rom.zip  # bypasses internal storage
```

## Battery Drain After Flash

**Issue:** Battery drains 20% per hour

**Fixes:**
1. Disable background sync
2. Run `adb shell dumpsys battery` to check for wakelocks
3. Disable Google Play Services telemetry
4. Flash kernel with undervolting support

## Recovery Won't Flash

**Issue:** TWRP fails with "Error executing updater"

**Causes:**
- ROM zip corrupted
- Updater-binary mismatch
- Device tree issue

**Fix:**
1. Verify zip: `unzip -t rom.zip`
2. Re-download ROM
3. Flash via adb sideload instead
