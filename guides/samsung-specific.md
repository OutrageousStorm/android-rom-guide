# Samsung-Specific Flashing Guide

Samsung has the most complex flashing process of any Android OEM. This guide covers everything Samsung-specific.

---

## Samsung tools

| Tool | Platform | Use |
|------|----------|-----|
| **Odin** | Windows only | Official Samsung flash tool |
| **Heimdall** | Linux/Mac/Win | Open-source Odin alternative |
| **TWRP** | Recovery | Custom recovery for most Samsung |

---

## Bootloader unlock (Samsung)

Samsung's bootloader unlock process:
1. Enable Developer Options (Settings → About → tap Build Number 7×)
2. Enable **OEM Unlocking** in Developer options
3. Reboot to Download Mode (hold Vol Down + Bixby + Power, or `adb reboot download`)
4. Long press Vol Up to unlock

> ⚠️ On recent Samsung flagships (S21+), OEM unlock may be **carrier-locked** for 7 days after activation. Must use the SIM the phone activated with.

> ⚠️ Knox counter trips permanently (KG State: Checking → Prenormal → Broken). No warranty after this.

---

## Flashing with Odin

```
1. Enter Download Mode
2. Open Odin on Windows
3. Load files:
   - BL → bootloader .tar.md5
   - AP → main firmware / ROM .tar.md5
   - CP → modem .tar.md5
   - CSC → country/carrier data (use HOME_CSC for data wipe, CSC for full)
4. Click Start
```

**Important:** Always use `HOME_CSC` if you want to keep your data. Using `CSC` wipes everything.

---

## TWRP on Samsung

Samsung uses `vbmeta` and `recovery-as-boot` on newer models. Method differs:

**Older Samsung (S9 and below):**
- Flash TWRP.tar via Odin to Recovery slot
- Hold Vol Down + Home + Power to boot recovery directly

**Newer Samsung (S10+, A52, S21 etc.):**
- Flash TWRP to `recovery` partition via Odin
- Some require patching `vbmeta` to disable verified boot

---

## One UI vs AOSP ROMs

| ROM type | Pros | Cons |
|----------|------|------|
| Stock One UI | Full Samsung features (DeX, Samsung Pay) | Bloat, ads, Knox |
| LineageOS | Clean AOSP, regular updates | No Samsung-specific features |
| crDroid | Heavy customization | Community support varies |
| GrapheneOS | ❌ Not available for Samsung | Pixel-only |

---

## Popular Samsung ROMs (by device)

### Galaxy S21 (p3s)
- LineageOS 21/22
- crDroid 10
- Evolution X

### Galaxy S23 (dm1q)  
- LineageOS 21 (unofficial)
- crDroid 10

### Galaxy A52s (a52sxq)
- LineageOS 20/21
- crDroid

---

## Knox & its implications

Knox is Samsung's security platform. Once tripped:
- Samsung Pay stops working permanently
- Knox Warranty Bit is set (visible in `*#*#9090#*#*`)
- Cannot be reset — even by Samsung service centers
- Does NOT affect AOSP ROM functionality

---

*Device pages: [ROM Haven wiki](https://romhaven.wikioasis.org)*
