# ROM Troubleshooting Guide

Common issues after flashing custom ROMs and their fixes.

## Boot Loop

If device gets stuck on bootanimation:
1. Hold Vol Down + Power to force reboot
2. Enter recovery (vol keys + power)
3. Wipe: Advanced Wipe → select Dalvik, Cache, System, Data
4. Reflash ROM via sideload: `adb sideload rom.zip`

## No Signal / Baseband Issues

Modem not flashed correctly.

**Via Odin (Samsung):**
- AP → ROM zip
- CP → modem.tar.md5
- CSC → country.tar.md5

**Via fastboot:**
```bash
fastboot flash radio radio.img
fastboot flash modem modem.img
```

## Stuck in Fastboot

```bash
fastboot flash boot boot.img
fastboot reboot
```

## Battery Drain

Let device settle first boot (2-3 hours). Then:
- Enable aggressive doze: `adb shell settings put global aggressive_doze_enabled 1`
- Check wakelocks: `adb bugreport > report.zip` (analyze with Battery Historian)
- Disable background sync for non-essential accounts

## Camera / Fingerprint Not Working

Ensure you have the correct ROM variant (codename must match exactly). Then:
- Check permissions: Settings → Apps → Camera → Permissions
- Reflash modem: `fastboot flash modem modem.img`

## SafetyNet / Play Integrity Fails

Install PlayIntegrityFix module via Magisk, or TrickyStore via LSPosed.

---

See android-rom-guide for full details.
