# Dirty Flash — Update ROM without wiping data

A **dirty flash** updates your ROM while keeping all your apps, settings, and data intact. Faster than clean flash but riskier.

## When to dirty flash

✅ **Safe:** point releases (12.0 → 12.1), same ROM branch, same device

❌ **Risky:** major versions (11 → 12), ROM switches, different base version

## Before you start

```bash
# Backup critical data
adb backup -apk -shared -all -f backup.ab

# Create TWRP backup
# (in recovery: Backup tab)
```

## Dirty flash procedure

```bash
1. Download new ROM zip for your device
2. Reboot to recovery (TWRP or LineageOS Recovery)
3. Flash the new ROM zip
4. **Skip wiping data/cache** — go directly to install
5. Optional: Flash Magisk (if using root)
6. Reboot
```

### TWRP method
```
Recovery → Install → select ROM.zip → Swipe to confirm
(don't wipe, don't factory reset, just install)
→ Reboot
```

### LineageOS stock recovery
```
Recovery → Apply update from ADB
adb sideload ROM.zip
```

## Potential issues after dirty flash

| Issue | Fix |
|-------|-----|
| Bootloop | Wipe /cache and /dalvik-cache, reboot. If still broken, clean flash. |
| Slow boot | Run `adb shell pm compile -r bg-dexopt` to recompile packages |
| App crashes | Clear app caches: `adb shell pm clear <package>` |
| WiFi/BT broken | Reboot, check system logs with `adb logcat` |
| Google Play broken | Clear Play Services: `adb shell pm clear com.google.android.gms` |

## Recovery in case of disaster

If dirty flash breaks your system:

### Option 1: Go back (if A/B device)
```bash
adb reboot bootloader
fastboot getvar current-slot
fastboot set_active a  # or b (opposite of current)
adb reboot
```

### Option 2: Clean flash from recovery
```bash
# Boot to recovery and select Factory Reset
# Then install ROM again
```

### Option 3: Return to stock firmware
```bash
adb reboot bootloader
fastboot flash system system.img
fastboot flash -w
fastboot reboot
```

## Pro tip: Dirty flash with Magisk survival

LineageOS A/B users can update without losing Magisk:

```bash
# In recovery:
1. Install ROM zip
2. Install Magisk zip
3. Boot (Magisk patched the new boot.img automatically)
```

## Safety checklist

- [ ] Backup important data
- [ ] Check device codename matches ROM
- [ ] Verify ROM release notes for known issues
- [ ] Keep TWRP backup available
- [ ] Have original firmware available
- [ ] Don't dirty flash across major versions

**Golden rule:** If you're unsure, do a clean flash. Data is replaceable; broken device is not.
