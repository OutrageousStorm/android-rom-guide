# Custom ROM Troubleshooting

Common issues and solutions.

## Bootloop

**Symptoms:** Phone stuck in boot animation or infinite restart

**Fixes:**
1. Boot to recovery: `adb reboot recovery`
2. Wipe cache: Recovery → Wipe Cache Partition
3. If still stuck: Format data and clean flash
4. Check logcat: `adb logcat | grep -i error`

**Common causes:**
- Flashed incompatible GApps
- Dirty flash from very different ROM
- Corrupted system partition

## Stuck on splash screen

**Might mean:** System is still loading (wait 2-3 minutes)

**If truly stuck:**
- Reboot to recovery
- Flash original stock ROM
- Restore from backup

## Apps crashing

**Try:**
1. Clear app cache: Settings → Apps → [app] → Clear Cache
2. Reinstall app
3. Wipe Dalvik cache in recovery

**If all apps crash:**
- May need clean flash
- Check if ROM is stable for your device

## No network/WiFi

**WiFi not detecting:**
- Reboot device
- Check if WiFi driver is in ROM
- May need to flash custom kernel with WiFi support

**Mobile data not working:**
- Check APN settings (should auto-populate)
- Try airplane mode toggle
- Check if modem firmware matches ROM version

## Battery drain

See: [Battery Optimization Guide](../guides/battery-optimization.md)

## Magisk not working

- Reboot after flashing
- Check if ROM disabled init.d
- Flash Magisk again

## Performance issues

- Check CPU frequency: `adb shell cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq`
- Try different governor (interactive, schedutil)
- May be thermal throttling — check temp

## Getting logs for help

```bash
# Last 100 lines of logcat
adb logcat -d | tail -100

# Save full dmesg
adb shell dmesg > dmesg.txt

# bugreport (comprehensive)
adb bugreport bugreport.zip
```

Share these when asking for help on XDA or GitHub!
