# ROM Flashing Troubleshooting

## Installation Issues

### "Error: Failed to verify payload"
Usually incorrect ROM for your device.
```bash
# Verify device codename
adb shell getprop ro.product.device
adb shell getprop ro.product.board

# Download ROM matching your exact device and build
```

### "No such file or directory" when flashing
Recovery can't find the ROM file on device.
```bash
# Use adb sideload instead
adb reboot recovery
# In recovery: Advanced → ADB Sideload
adb sideload rom.zip
```

### Boot loop after ROM flash
Usually a bad wipe or incompatible GApps.
```bash
# Boot to recovery and restore previous backup
# Or: full factory reset (Advanced Wipe → all partitions)
```

### "Signature verification failed"
TWRP can't verify ROM signature (may be intentional on some ROMs).
```bash
# In TWRP: Wipe → Advanced Wipe → uncheck "Verify ZIP signature"
# Then try flashing again
```

### Bootloader won't unlock on Samsung
Samsung may have bootloader locked by carrier (T-Mobile).
```bash
# Check if unlockable
adb reboot bootloader
fastboot getvar (bootloader)

# If it says "locked - carrier", you need original carrier SIM
```

---

## Post-Flash Issues

### Phone gets stuck on boot logo
```bash
# Try booting to recovery first:
adb reboot recovery

# Then factory reset from recovery:
# Wipe → Advanced Wipe → Dalvik, Cache, Data, System
# Reflash ROM + GApps
```

### Certain apps force close
Usually a GApps incompatibility or missing dependencies.
```bash
# Try reflashing with a smaller GApps package (pico instead of full)
# Or use microG instead of Google Play
```

### No mobile network / SIM not detected
Device tree or modem issue — ROM may not have proper radio drivers.
```bash
# Check if modem.img needs to be flashed separately
# Some ROMs require: fastboot flash radio modem.img

# Or try reflashing stock ROM via ADB/Odin and starting over
```

### WiFi doesn't work
Usually a driver issue — try different ROM or check if kernel includes WiFi modules.
```bash
# From LineageOS, try a different branch or older build
```

---

## Security & Root Issues

### Banking app won't open after root
SafetyNet/Play Integrity failing.
```bash
# Install PlayIntegrityFix (Magisk module)
# Then install TrickyStore (LSPosed module) for extra hardening
# Reboot and test
```

### "Device not certified" Google Play error
Play Integrity check failing.
```bash
# Option 1: Install PlayIntegrityFix module + reboot
# Option 2: Disable Google Play Integrity in developer settings
# Option 3: Use Aurora Store instead of Play Store (no certification check)
```

### Root detected by security app
Try using Shamiko + DenyList on your banking app.
```bash
# Magisk → Settings → Configure DenyList
# Add com.example.bankapp (check your bank's package name)
# Also enable Zygisk in Magisk settings
# Reboot
```

---

## Performance Issues

### Phone feels slow after ROM flash
Usually needs optimization or tweaking.
```bash
# Disable background processes: Settings → Apps → [app] → Battery → Background restriction
# Clear cache: Settings → Storage → Cached Data → Clear
# Disable animations: Settings → Developer Options → Animation scale → 0x
```

### Battery drains quickly
Check what's keeping device awake.
```bash
python3 android-wakelock-analyzer.py bugreport.zip
# Identify top wakelock culprits and restrict background for those apps
```

### Overheating
Usually bad kernel or thermal management.
```bash
# Try a different kernel version or revert to stock kernel
# Check Settings → Display → Adaptive battery → Off temporarily
```
