# ROM Flashing Troubleshooting

Common issues and fixes when flashing custom ROMs.

## Boot Loops

### Symptom: Device boots to logo then reboots infinitely

**Cause 1: GApps wrong version**
- Solution: Flash correct GApps for your Android version
- Example: Android 13 ROM needs Android 13 GApps

**Cause 2: Magisk module conflicts**
```bash
# Boot to recovery, disable all modules
# Or boot with power button held (skip modules)
# Then remove the bad module
```

**Cause 3: Incompatible recovery**
- Flash matching TWRP version for your ROM
- Some ROMs need newer TWRP than others

### Symptom: Boots fine but apps crash immediately

**Cause: Conflicting Magisk module**
```bash
adb disable-verity                    # disable dm-verity temporarily
adb wait-for-recovery
adb sideload twrp.zip                 # boot to recovery
# In TWRP: disable Magisk in modules
```

## Installation Errors

### "Signature verification failed"

**In TWRP:**
- Go to Wipe → Format Data (not just clear)
- Or: Settings → turn off signature verification

**Via Magisk:**
- Flash after ROM, not before

### "This build is for OnePlus 9, this device is..."

**Cause: Flashing ROM for wrong device**
- Check device codename: `adb shell getprop ro.product.device`
- Re-download correct ROM

### "Not enough space"

**Solution:**
```bash
adb sideload rom.zip          # instead of TWRP install from /sdcard
```

## Post-Flash Issues

### No network / WiFi greyed out

**Symptom: WiFi toggle disabled after flash**

```bash
# Reboot to recovery
# Advanced → Terminal
adb shell rm /data/misc/wifi/*
adb shell reboot
```

Or reset WiFi via settings after first boot.

### Battery drains fast

**Check:**
```bash
# See what's holding wakelocks
adb shell dumpsys batterystats | grep WAKE_LOCK

# GMS draining? Install:
# Magisk → GMS Doze module
```

### Safetynet / Play Integrity fails

**Install:**
- PlayIntegrityFix (Magisk module)
- TrickyStore (LSPosed module) for banking apps

### Apps force-close

**Try:**
```bash
adb shell pm clear com.android.systemui
adb reboot
```

Or do a clean install (wipe data).

## Recovery Won't Boot

### Symptom: Can't boot to TWRP

**If on fastboot:**
```bash
fastboot boot twrp.img          # temp boot
# Then in TWRP: Install → Install Recovery Ramdisk
```

**If stuck on logo:**
```bash
fastboot flash boot twrp.img    # flash as boot
fastboot reboot recovery
```

## Reverting to Stock

**Pixel:**
```bash
# Download factory image from https://developers.google.com/android/images
unzip bluejay-factory-XXXX.zip
cd bluejay-factory-XXXX
./flash-all.sh
```

**Samsung:**
```bash
# Download via SmartSwitch or from sammobile
# Flash via Odin
```

**Generic:**
```bash
fastboot -w update image.zip  # wipes data
```

## Performance Issues

### Sluggish after flash

**Try:**
```bash
# Clear system cache
adb shell pm trim-caches 100G

# Disable unused sensors
adb shell settings put secure sensor_default_mode 0

# Reboot
adb reboot
```

### High idle battery drain

**Disable in settings:**
- Location history
- WiFi scanning
- Google activity

**Or install:**
- GMS Doze Magisk module
- Disable background location

## Asking for Help

When posting a brick log:
1. ROM name and version
2. Device model + codename
3. Recovery version
4. Last action taken
5. Serial output from TWRP if available
6. Boot.log (TWRP → Advanced → View Log)
