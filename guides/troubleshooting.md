# ROM Troubleshooting Guide

Common issues after flashing a ROM and how to fix them.

## Bootloop / Doesn't boot

**Signs:** Device gets stuck on splash screen or boot animation.

**Fix:**
```bash
# Boot to TWRP recovery
adb reboot recovery

# Wipe everything (from TWRP: Wipe → Advanced Wipe → select all)
adb sideload rom.zip
adb sideload gapps.zip
adb sideload magisk.zip

# Reboot
adb reboot
```

If still looping after 10 minutes, flash stock ROM via fastboot/Odin.

---

## "Unfortunately, X has stopped" crashes

**Cause:** Missing GApps or GMS issues.

**Fix:**
1. Boot to TWRP
2. Flash GApps again (MindTheGapps nano or pico)
3. Wipe Dalvik/ART Cache → Advanced Wipe → Dalvik/ART Cache
4. Reboot

---

## No data/slow network

**Cause:** Radio firmware mismatch or incorrect region settings.

**Fix:**
```bash
# Check if radio was flashed (device-specific)
# For Samsung: Odin → AP slot includes radio
# For others: separate radio.img flash via fastboot

fastboot flash modem modem.img  # if available
fastboot reboot

# Set region in settings (some ROMs require this)
```

---

## Google Play won't load apps / Play Integrity fails

**Cause:** Rooted device, custom ROM, or modified build props.

**Fix:**
```bash
# Install PlayIntegrityFix module (via Magisk)
# Or install TrickyStore (LSPosed module)

# Check status
adb shell getprop ro.build.fingerprint  # should match official build
```

---

## Battery drain (waking constantly)

**Signs:** Phone gets hot, won't stay asleep.

**Cause:** App misbehavior, sync settings, or location polling.

**Fix:**
```bash
# See what's holding wake locks
adb shell dumpsys battery | grep wake
adb shell dumpsys power | grep -A 20 "WAKE_LOCK_HELD"

# Disable sync for unused accounts (Settings → Accounts)
# Disable location (Settings → Location)
# Restrict background for problem apps (Settings → Battery → Background usage limits)
```

---

## Camera/Fingerprint/NFC not working

**Cause:** Device tree issues, missing blobs, or hardware HAL mismatch.

**Fix:**
1. Flash latest TWRP for your device (camera requires proper recovery)
2. Use a ROM specifically built for your device (not GSI)
3. If on GSI + missing drivers, try a device-specific ROM instead

---

## "No such file or directory" during flash

**Cause:** Corrupted ROM zip or wrong file path.

**Fix:**
```bash
# Check zip integrity
unzip -t rom.zip  # should show "No errors"

# Use absolute path
adb sideload /full/path/to/rom.zip

# Or push to device first
adb push rom.zip /sdcard/
adb shell cd /sdcard && unzip -t rom.zip
```

---

## ROM keeps asking for setup after each reboot

**Cause:** Factory reset flag not cleared or data encryption issue.

**Fix:**
```bash
# Wipe data completely from TWRP
# Make sure encryption is compatible with ROM
# Disable forced encryption if needed (device-specific)
```
