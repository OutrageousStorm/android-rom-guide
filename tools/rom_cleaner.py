#!/usr/bin/env python3
"""
rom_cleaner.py -- Remove bloat from flashed ROMs (GApps, Facebook, etc.)
Use before first boot or after flash to minimize bloat.
Usage: python3 rom_cleaner.py --list
       python3 rom_cleaner.py --remove facebook,tiktok,google-apps
"""
import argparse, os

BLOAT = {
    "google-apps": [
        "GoogleFeedback.apk", "GooglePartnerSetup.apk", "Maps.apk",
        "Velvet.apk", "Chrome.apk", "Drive.apk", "Duo.apk",
    ],
    "facebook": [
        "Facebook.apk", "Instagram.apk", "Messenger.apk", "WhatsApp.apk",
    ],
    "ads": [
        "GoogleAdService.apk", "Gmail.apk",  # Gmail has aggressive ads
    ],
    "xiaomi": [
        "XMiuiBrowser.apk", "MSA.apk", "MiuiCompass.apk",
        "MiuiSecurityCenter.apk", "MiuiSuperMarketO2O.apk",
    ],
    "samsung": [
        "Samsung*.apk", "OnDrive.apk", "BixbyVoice.apk",
    ],
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", action="store_true", help="List bloat categories")
    parser.add_argument("--remove", help="Bloat to remove (comma-sep)")
    parser.add_argument("--rom-path", default=".", help="Path to extracted ROM")
    args = parser.parse_args()

    if args.list:
        print("\nAvailable bloat categories:")
        for cat, files in BLOAT.items():
            print(f"  {cat:<15} {len(files)} files")
        print("\nUsage: python3 rom_cleaner.py --remove google-apps,facebook")
        return

    if not args.remove:
        print("Use --list to see categories or --remove cat1,cat2 to clean")
        return

    categories = args.remove.split(",")
    print(f"\n🧹 ROM Cleaner — removing bloat from {args.rom_path}")
    removed = 0

    for cat in categories:
        cat = cat.strip()
        if cat not in BLOAT:
            print(f"  ❌ Unknown category: {cat}")
            continue

        for pattern in BLOAT[cat]:
            # Search through ROM structure
            for root, dirs, files in os.walk(args.rom_path):
                for f in files:
                    if pattern.replace("*", "") in f:
                        fpath = os.path.join(root, f)
                        try:
                            os.remove(fpath)
                            print(f"  ✓ removed: {f}")
                            removed += 1
                        except Exception as e:
                            print(f"  ✗ {f}: {e}")

    print(f"\n✅ Cleaned {removed} files. Re-package ROM and flash.")

if __name__ == "__main__":
    main()
