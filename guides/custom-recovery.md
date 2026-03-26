# Custom Recovery Guide

Custom recoveries replace the stock Android recovery, enabling ROM flashing, backups, and advanced maintenance.

---

## Major custom recoveries

| Recovery | Pros | Cons |
|----------|------|------|
| **TWRP** | Most compatible, huge device support | Older UI, slower updates |
| **OrangeFox** | Modern UI, built-in Magisk installer | Fewer devices |
| **SHRP (SkyHawk)** | Nice UI, dashboard feel | Limited device support |
| **PBRP (Pitch Black)** | Clean dark theme | Niche |
| **LineageOS Recovery** | Minimal, built into LineageOS | Less features |

---

## Finding recovery for your device

```
TWRP:       https://twrp.me/Devices/
OrangeFox:  https://orangefox.download/
SHRP:       https://shrp.github.io/
XDA:        https://forum.xda-developers.com (search "[device] TWRP")
```

---

## Flashing TWRP

### Fastboot method (most devices)
```bash
adb reboot bootloader
fastboot flash recovery twrp.img
fastboot reboot recovery     # boot into recovery immediately
```

### Temp boot (safer first time)
```bash
fastboot boot twrp.img       # boots recovery without flashing
                             # use this to install TWRP permanently from within
```

### Samsung (via Odin)
- Open Odin → AP slot → select twrp.tar.md5
- Click Start
- Immediately hold Vol Down + Home + Power after screen goes black to boot recovery

---

## Core TWRP operations

```
Wipe → Advanced Wipe → check: Dalvik/ART Cache, Cache, System, Data
Install → navigate to ROM zip → Swipe to install
Backup → select partitions (Boot, System, Data) → Swipe to backup
Restore → select backup → Swipe to restore
Advanced → ADB Sideload → on PC: adb sideload rom.zip
```

---

## ADB Sideload (recommended for clean installs)

```bash
# In TWRP: Advanced → ADB Sideload → swipe to start

# On PC:
adb sideload rom.zip
adb sideload gapps.zip    # if needed
adb sideload magisk.zip   # if rooting
```

---

## Partition types

| Partition | Contents | Wipe for clean install? |
|-----------|----------|------------------------|
| Boot | Kernel + ramdisk | Yes (flashed by ROM) |
| System | Android OS | Yes (ROM installs here) |
| Data | User data, apps | Yes (factory reset) |
| Cache | App cache | Yes |
| Dalvik/ART | Compiled app code | Yes |
| Vendor | Hardware drivers | Sometimes (ROM-specific) |
| Radio/Modem | Baseband firmware | No (flash separately) |

---

## Backup before anything

TWRP backup saves everything — you can restore even if flash goes wrong:
```
Backup → select Boot + System + Data → give it a name → Swipe
# Backup saved to /sdcard/TWRP/BACKUPS/
```

Pull backup to PC:
```bash
adb pull /sdcard/TWRP/BACKUPS/ ./twrp-backup/
```
