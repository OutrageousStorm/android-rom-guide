# LineageOS Deep Dive

LineageOS is the most installed custom ROM. Here's how to master it.

## Installation variants

| Variant | What it is | Best for |
|---------|-----------|----------|
| **Standard LineageOS** | Pure AOSP + updates | Daily drivers, stability |
| **LineageOS for microG** | Built-in microG | Privacy without Play Services |
| **LineageOS GoLinks** | With NanoGapps | Minimal Google integration |

## Post-install tweaks

After flashing LineageOS, customize in Settings:

```
System → Developer Options → Enable:
  □ USB Debugging
  □ Rooted Debugging (if Magisk installed)
  □ Android Debugging over Network (if on WiFi)

System → Languages & input:
  □ Spell checker (auto-learn disabled)
  □ Suggest contacts (disabled for privacy)

Notifications → Advanced:
  □ Show lock screen notifications: OFF (if paranoid)

About phone → Build number: tap 7×
```

## Common post-install issues

| Problem | Solution |
|---------|----------|
| No system updates offered | Check Settings → About → System update |
| Camera broken | Reflash camera vendor from original ROM |
| Fingerprint not working | May require separate driver, check XDA |
| GPS drifting | Calibrate compass: Compass app → calibrate |
| Battery drain | Disable location history, WiFi scanning |

## Customization via Magisk modules

With Magisk installed:

```
Recommended modules for LineageOS:
  - Universal GMS Doze (battery)
  - Shamiko + ZygiskNext (advanced hiding)
  - Font Manager (custom fonts)
  - Navbar Apps (quick app launcher)
```

## Backup strategy

Before flashing anything:

```bash
# In TWRP:
Backup → Boot, System, Data, Vendor → Swipe
# This lets you restore in seconds if something breaks
```

## OTA updates with Magisk

LineageOS releases OTA updates monthly. To survive them with Magisk:

1. Magisk app → Install → Install to Inactive Slot (After OTA)
2. Settings → System update → Download & Install
3. Reboot — Magisk patches the new boot partition automatically
4. Next reboot: Magisk still active

## Performance tuning for LineageOS

```bash
# Via ADB, after flashing
adb shell settings put global power_efficient_workqueue_enabled 1
adb shell settings put system screen_brightness_mode 1  # auto brightness
adb shell settings put global disable_window_anim_scale 1
```

## Debugging LineageOS

Check system logs:

```bash
adb logcat | grep -i error
adb logcat | grep -i warning | head -20
adb bugreport bugreport.zip
```
