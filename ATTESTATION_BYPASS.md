# SafetyNet & Play Integrity Bypass

How to pass hardware attestation checks on custom ROMs + rooted devices.

## The problem

**SafetyNet** (deprecated) and **Play Integrity API** check:
- Device fingerprint (exact model)
- Bootloader lock status
- SELinux enforcing mode
- System modifications detected
- Magisk root detected

Banking apps, Google Pay, and some games require these checks.

## Solutions

### 1. PlayIntegrityFix + TrickyStore (Best)

Install these Magisk modules in order:

```bash
# In Magisk Manager → Modules → search:
1. PlayIntegrityFix
2. TrickyStore  # For hardware-level attestation
```

**What they do:**
- PlayIntegrityFix patches the Play Integrity library before it loads
- TrickyStore spoofs hardware identifiers at the kernel level
- Combined: passes even strict banking app checks

**Success rate:** 95%+

```bash
# Test
adb shell am start -n com.google.android.gms/.chimera.GmsIntegrityChimeraActivity
# Should show "PASSED"
```

### 2. Shamiko + PlayIntegrityFix (Alternative)

If TrickyStore doesn't work:

```bash
# Install in Magisk:
1. PlayIntegrityFix
2. Shamiko  # Better root hiding than DenyList
```

Enable **Zygisk** in Magisk settings first.

### 3. Manual approach (advanced)

Spoof build props:

```bash
# In Magisk module init.rc:
resetprop ro.build.fingerprint "google/crosshatch/crosshatch:11/RP1A.201005.004.A1/5891938:user/release-keys"
resetprop ro.build.version.security_patch "2021-12-05"
resetprop ro.boot.verifiedbootstate "green"
resetprop ro.boot.veritymode "enforcing"
```

**Limitation:** Only passes basic checks, not hardware attestation.

## Testing

### Check attestation status
```bash
# Test Play Integrity (requires PlayIntegrityFix)
adb shell am start com.google.android.gms/.chimera.GmsIntegrityChimeraActivity

# Logcat output:
# If sees "PASSED" = works
# If sees "FAILED" = need TrickyStore or different approach
```

### Test with real apps

| App | Check Type | Bypass |
|-----|-----------|--------|
| Google Pay | Hardware + Basic | TrickyStore + PlayIntegrityFix |
| Pokemon Go | Basic only | PlayIntegrityFix alone |
| Banking (most) | Hardware | TrickyStore + PlayIntegrityFix |
| Google Play Store | Basic | PlayIntegrityFix alone |

## DenyList strategy (Magisk)

Even with PlayIntegrityFix, some apps detect root directly. Add them to **Magisk → Settings → DenyList**:

```
com.google.android.gms
com.google.android.apps.payments
com.google.android.apps.authentication
com.google.android.as
```

When an app is in DenyList:
- Root is hidden from that app's process
- Magisk modules don't apply to it
- Safe to use banking/payment apps

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Play Integrity still fails | Install TrickyStore (requires Pixel/MIUI-like device) |
| Banking app closes | Add to DenyList in Magisk |
| After OTA, checks fail | Reflash PlayIntegrityFix in recovery |
| "Hardware attestation failed" | Your device's bootloader may be incompatible |

**Note:** Some banking apps require exact bootloader + device props. If they still fail after all this, the ROM is incompatible with that app.
