# Common ROM Issues & Fixes

## Bootloop

**Symptoms:** Device loops at boot animation, doesn't reach home screen.

**Diagnosis:**
```bash
# Check last boot logs
adb shell cat /data/anr/traces.txt | tail -50

# Or via logcat from recovery
adb logcat
```

**Fixes:**
1. Wait 5+ minutes — first boot can take a while
2. Clear cache in recovery: Wipe → Dalvik/ART Cache
3. Factory reset if above fails
4. Try a different ROM version
5. Check if ROM is compatible with device model

## No signal / Modem issues

**Symptoms:** No bars, can't make calls, no mobile data.

**Fixes:**
```bash
# Toggle airplane mode
adb shell settings put global airplane_mode_on 1
adb shell settings put global airplane_mode_on 0

# Reset radio
adb shell setprop persist.sys.usb.config adb
adb reboot

# Check modem logs (advanced)
adb logcat | grep -i "radio\|modem\|ril"
```

If still broken: ROM may not include modem firmware for your device.

## WiFi won't connect

**Solutions:**
```bash
# Forget and rescan
adb shell cmd wifi forget-network <SSID>
adb shell cmd wifi scan-result

# Reset WiFi
adb shell settings put secure wifi_enabled 0
sleep 2
adb shell settings put secure wifi_enabled 1

# Check WiFi logs
adb logcat | grep -i "wifi\|wpa"
```

## Camera/RIL/GPS not working

These are device-specific HALs. Some custom ROMs don't include them:

**For LineageOS:**
- Download the device-specific ZIP (microG or official builds)
- Ensure you flashed the correct device codename

**For AOSP GSIs:**
- Try a different vendor partition
- Use `fastboot erase vendor` and let ROM provide it

## Battery drain

See: [Battery Optimization](battery-optimization.md)

## Encryption errors

```bash
# Factory reset (wipes everything but ROM)
adb shell recovery --wipe_data
```
