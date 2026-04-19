# Android ROM Performance Optimization

Making your custom ROM fast — CPU scaling, I/O tweaks, thermal management.

---

## CPU Governors (with custom kernel)

Best default governors:
- **schedutil** (modern, recommended) — frequency follows scheduler load
- **interactive** (responsive) — fast ramp-up, balances performance/battery
- **performance** (max speed) — always at max freq, hottest
- **conservative** (battery) — slow ramp-up, steps down gradually

```bash
# Check current governor
adb shell cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor

# Change (requires root via Magisk/kernel)
adb shell su -c "echo schedutil > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"
```

---

## I/O Scheduler Tuning

```bash
# Check scheduler
adb shell cat /sys/block/sda/queue/scheduler

# Best for eMMC/NAND: deadline or mq-deadline
adb shell su -c "echo mq-deadline > /sys/block/sda/queue/scheduler"

# Read-ahead optimization
adb shell su -c "echo 2048 > /sys/block/sda/queue/read_ahead_kb"
```

---

## Disable Unnecessary Services

Via ADB (no root):
```bash
# Disable background WiFi scanning
adb shell settings put global wifi_scan_always_enabled 0

# Disable BLE scanning
adb shell settings put global ble_scan_always_enabled 0

# Limit background processes
adb shell settings put global background_process_limit 3
```

---

## Zram (Compressed RAM)

Magisk module: **Zram Mod** — allocates compressed swap to speed up low-memory scenarios

---

## Thermal Throttling

Some kernels expose thermal control:
```bash
# Check temperature
adb shell cat /sys/class/thermal/thermal_zone0/temp  # output in millidegrees

# Adjust thermal throttle (if supported)
adb shell su -c "echo 75000 > /sys/class/thermal/thermal_zone0/trip_point_0_temp"
```

---

## Animation Speeds

```bash
# Reduce system animation duration (0 to 1.0, default 1.0)
adb shell settings put global animator_duration_scale 0.5

# Reduce transition animation (0 to 1.0)
adb shell settings put global transition_animation_scale 0.5

# Instant for power users
adb shell settings put global animator_duration_scale 0.0
```

---

## Storage Optimization

Via ADB:
```bash
# Trim free space (speeds up writes)
adb shell su -c "fstrim -v /data"

# Check storage health
adb shell dumpsys batterystats | grep "mHoldingDisplaySuspendBlocker"
```

---

## Per-ROM Tweaks

### LineageOS
- Settings → Developer Options → Increase logger buffer sizes
- Settings → Storage → Optimize storage (runs defrag-like operation)

### crDroid
- Settings → System → Miscellaneous → Disable Bluetooth audio routing for multiple devices

### GrapheneOS
- Settings → System → Auto-reboot feature helps keep memory clean
