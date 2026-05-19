# Samsung Firmware Flashing (2024-2026)

Complete guide for flashing Samsung stock firmware via Odin or Heimdall.

## Get firmware

- **SamFirm** — download official firmware: https://www.sammobile.com
- **Samsung Firmware Download** — https://samsung-firmware.firmware.to
- **SmartSwitch** — Samsung's official tool (Windows/Mac)

## Flash with Odin (Windows)

```
1. Extract firmware .tar.md5 file
2. Boot device to Download Mode: Power + Home + VolDown
3. Open Odin → select .tar.md5 in AP slot
4. Auto Reboot + F. Reset Time checked
5. Click Start
6. Device reboots automatically
```

## Flash with Heimdall (Mac/Linux)

```bash
heimdall flash --RECOVERY recovery.img --SYSTEM system.img --BOOT boot.img
```

## Known issues

- **Bootloader locked after flash** — expected, SafetyNet will pass
- **CSC changes region** — use PIT file to preserve, or reflash to change
- **"Phone is already in use"** — toggle USB debugging off/on

## Preserve data while flashing

Only OTA updates preserve data. Full firmware flash = wipe.

To save data: extract data via TWRP first, then restore after flash.
