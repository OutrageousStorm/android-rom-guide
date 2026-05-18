#!/usr/bin/env python3
"""
rom_downloader.py -- Download latest custom ROM for your device
Usage: python3 rom_downloader.py --rom lineageos --device redmi_note_11
"""
import subprocess, json, argparse, sys

ROM_SOURCES = {
    "lineageos": "https://api.lineageos.org/v1/devices",
    "crDroid": "https://crdroid.net/api/devices",
}

def fetch_json(url):
    r = subprocess.run(f"curl -s '{url}'", shell=True, capture_output=True, text=True)
    try: return json.loads(r.stdout)
    except: return None

def find_lineageos(device):
    data = fetch_json(f"{ROM_SOURCES['lineageos']}/{device}/builds")
    if not data or 'response' not in data or not data['response']:
        return None
    latest = data['response'][0]
    return {
        'rom': 'LineageOS',
        'version': latest.get('version', 'latest'),
        'size_mb': latest.get('size', 0) / (1024*1024),
        'date': latest.get('datetime', ''),
        'filename': latest.get('filename', '')
    }

def main():
    parser = argparse.ArgumentParser(description="Download latest custom ROM")
    parser.add_argument("--rom", choices=list(ROM_SOURCES.keys()))
    parser.add_argument("--device", help="Device codename")
    args = parser.parse_args()

    if not args.rom or not args.device:
        print("Usage: python3 rom_downloader.py --rom lineageos --device redmi_note_11")
        sys.exit(1)

    print(f"Searching {args.rom} for {args.device}...")

    if args.rom == "lineageos":
        result = find_lineageos(args.device)
    else:
        result = None

    if not result:
        print(f"No builds found for {args.device}")
        return

    print(f"ROM: {result['rom']}")
    print(f"Version: {result.get('version', 'unknown')}")
    print(f"Size: {result.get('size_mb', 0):.0f} MB")
    print(f"Filename: {result.get('filename', '')}")

if __name__ == "__main__":
    main()
