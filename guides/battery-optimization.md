# Battery Optimization Guide

Getting the most battery life from a custom ROM.

---

## Why custom ROMs can drain more battery

- No OEM optimizations for specific hardware
- Different thermal management
- GApps running extra background services
- Debug logging enabled in some builds

---

## Quick wins (no root)

### 1. Aggressive doze
```bash
# Enable aggressive doze (restricts background wakeups)
adb shell dumpsys deviceidle enable deep
adb shell dumpsys deviceidle enable light
adb shell dumpsys deviceidle step deep
```

### 2. Disable wake locks from problem apps
```bash
# See what's holding wake locks
adb shell dumpsys power | grep "WAKE_LOCK_HELD"
adb shell dumpsys battery | grep "wake"

# Identify battery hogs
adb shell dumpsys batterystats | grep "uid" | sort -t= -k2 -rn | head -20
```

### 3. Restrict background for GApps
```bash
# Put GMS into doze aggressively
adb shell dumpsys deviceidle whitelist -com.google.android.gms
adb shell am set-inactive com.google.android.gms true
```

### 4. Disable unused radio
```bash
adb shell settings put global wifi_on 0        # WiFi off when not needed
adb shell settings put global bluetooth_on 0   # BT off
# Or just toggle in quick settings
```

---

## With Magisk (root)

### Universal GMS Doze module
Puts Google Play Services into deep doze — one of the highest-impact battery mods available:
- Install from Magisk repo: search "Universal GMS Doze"
- Reboot
- Expect 15-30% improvement in standby drain

### ACC (Advanced Charging Controller)
Limits charge to 80-85% to preserve long-term battery health:
```bash
# After installing ACC Magisk module
acc -e 80   # charge to 80%, stop
acc -d 75   # resume charging at 75%
```

### Thermal tweaks
Some kernels expose thermal control:
```bash
# Check thermal zones
cat /sys/class/thermal/thermal_zone*/type
cat /sys/class/thermal/thermal_zone*/temp

# Custom kernels often include a thermal profile switcher
```

---

## Per-ROM tips

### LineageOS
- Settings → Battery → Background process limit → set to 3-4 processes
- Enable "Turn off screen during calls"

### crDroid / Evolution X
- These have a built-in "Performance Profile" — set to Battery or Balanced
- Gaming mode eats battery fast — disable if not gaming

### GrapheneOS
- Auto-reboot feature is power-neutral (triggers from inactivity anyway)
- Network toggle per-app — block background apps from using data

---

## Diagnosing drain with Battery Historian

```bash
# Reset battery stats
adb shell dumpsys batterystats --reset

# Use device for a few hours, then:
adb bugreport > bugreport.zip

# Open https://bathist.ef.lc/ and upload bugreport.zip
# See per-app wakelocks, CPU time, network usage
```
