# Samsung Custom ROM Flashing

Samsung devices require special steps due to Knox, FRP locks, and Samsung-specific partitions.

## Pre-requisites

- **Odin3** (Windows) or **Heimdall** (Linux/Mac) — Samsung-specific flashing tool
- **Custom ROM zip** — built for your exact Samsung model
- **TWRP** — optional but recommended (for sideload method)
- **USB debugging** and **OEM unlock** enabled
- **Stock bootloader/bootimage** for your device (optional, for recovery)

## Method 1: Odin (Windows — Easiest)

### 1. Download files
- ROM file: `lineage-xx.x-20xx-UNOFFICIAL-<model>.zip`
- Odin: https://github.com/medaiyoushi/Odin3
- USB drivers: Samsung official drivers (Zadig on Windows if needed)

### 2. Download mode on device
```
Power off device
Hold: Vol Down + Power + Home (exact combo varies by model)
Wait for "Downloading..." screen
Press Vol Up to confirm
```

### 3. Open Odin
- Select downloaded ROM file in **AP** slot
- Leave other slots empty (BL, CP, CSC will be in the ROM)
- Select correct COM port
- Click **Start**

### 4. Wait
- Flashing takes 5-15 minutes
- Device will reboot automatically
- First boot takes 2-3 minutes

---

## Method 2: Heimdall (Linux/Mac)

```bash
# Download Heimdall
wget https://releases.glassechidna.com.au/heimdall/Heimdall-Linux.tar.gz
tar xzf Heimdall-Linux.tar.gz

# Boot to Download Mode (same as above)

# Flash
./heimdall flash --kernel boot.img --system system.img --recovery recovery.img \
  --cache cache.img --datafs userdata.img --hidden hidden.img
```

---

## Method 3: TWRP Sideload (If Download Mode fails)

```bash
# Boot to recovery (hold Vol Up + Power + Home or Recovery key combo)
# In TWRP: Advanced → ADB Sideload

# On PC:
adb sideload lineage-xx.x-<model>.zip
```

---

## Partition Layout (Samsung Devices)

Samsung uses different partitions than stock AOSP:

| Partition | Purpose | Tool |
|-----------|---------|------|
| `boot` | Kernel | odin AP |
| `system` | System image | odin AP |
| `cache` | Cache partition | odin AP |
| `hidden` | Samsung hidden partition | odin AP (keep original) |
| `efs` | IMEI/modem data | **DO NOT FLASH** |
| `recovery` | Recovery image | odin AP |

**Pro tip:** Keep `efs` and `hidden` partitions from stock. Flashing wrong data causes IMEI corruption.

---

## Common Issues

### Bootloop after flash
- Let device sit for 5 minutes (initializing)
- If persists: wipe cache + dalvik in TWRP recovery
- If still bootloop: flash stock firmware then try ROM again

### Odin error: `FAIL (Auth)` or `SECURITY ERROR`
- Device Knox is tripped
- Solution: Flash the ROM without `--unified` in Odin if available
- Or: Use TWRP sideload method instead

### No recovery partition after flash
- Some ROMs don't include recovery
- Boot to TWRP, flash Magisk + TWRP installer again

### Device not detected in Odin
- Install Samsung USB drivers: https://developer.samsung.com/android-usb-drivers
- Or use **Zadig** to install libusbK driver
- Try different USB port (prefer USB 2.0 on older boards)

---

## Verify Successful Flash

```bash
adb shell getprop ro.build.fingerprint
# Should show your ROM's build fingerprint
```

