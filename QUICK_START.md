# Android ROM Quick-Start (10 minutes)

TL;DR version — just the essentials.

## Step 1: Unlock Bootloader (5 min)

**Pixel/OnePlus:** Fastest
```bash
adb reboot bootloader
fastboot flashing unlock
# Device wipes. Tap to confirm on screen.
adb reboot
```

**Samsung:** Slower (carrier dependent)
- Settings → About → tap Build Number 7× → OEM Unlocking
- Reboot to Download Mode: Vol Down + Bixby + Power
- Open Odin → select recovery.tar.md5 in BL slot → Start
- Takes 5-10 min

**Xiaomi:** Waiting required
- https://unlock.mi.com — apply, wait 30-72 hours
- Then use `Mi Unlock Tool` (Windows only, unfortunately)

## Step 2: Flash Recovery (2 min)

```bash
adb reboot bootloader
fastboot flash recovery twrp.img   # or your recovery of choice
fastboot reboot recovery
```

## Step 3: Flash ROM (2 min)

In TWRP recovery:
```
Install → Select ROM.zip → Swipe to install
(optionally install GApps.zip, then Magisk.zip)
Reboot System
```

Boom. You're done. First boot takes 30-60 seconds while it optimizes.

---

## What to do after

1. **Check for updates:** Most ROMs auto-update now
2. **If you want root:** Install Magisk via Magisk Manager app
3. **If you want privacy:** Check [android-privacy-guide](https://github.com/OutrageousStorm/android-privacy-guide)
4. **If things break:** Boot to TWRP, restore backup (you made one, right?)

---

## Common issues

| Problem | Fix |
|---------|-----|
| Boot loop | Boot to recovery, wipe Cache + Dalvik, reboot |
| Can't mount /data | Factory reset in TWRP (Wipe → Format Data) |
| SafetyNet fails | Install PlayIntegrityFix Magisk module |
| Google apps missing | Flash GApps before first boot |
| No cellular | Flash modem/radio firmware from factory image |

---

**Full guide:** See [android-rom-guide](https://github.com/OutrageousStorm/android-rom-guide)
