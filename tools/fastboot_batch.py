#!/usr/bin/env python3
"""
fastboot_batch.py -- Batch fastboot operations (flash multiple partitions at once)
Useful: when you have 20 devices to flash, or testing many ROM versions

Usage:
  python3 fastboot_batch.py --device <serial> --flash-all rom_build/
  python3 fastboot_batch.py --batch devices.txt --image recovery.img
  python3 fastboot_batch.py --erase system,vendor,userdata
"""
import subprocess, sys, glob, argparse, time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

def fastboot(cmd, serial=None, timeout=60):
    full = ['fastboot']
    if serial: full += ['-s', serial]
    full += cmd.split()
    try:
        r = subprocess.run(full, capture_output=True, text=True, timeout=timeout)
        return r.returncode == 0, r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT"

def list_devices():
    r = subprocess.run(['fastboot', 'devices'], capture_output=True, text=True)
    return [l.split()[0] for l in r.stdout.splitlines() if l.strip()]

def flash_partition(serial, partition, image):
    ok, msg = fastboot(f'flash {partition} {image}', serial=serial)
    status = '✓' if ok else '✗'
    print(f"  {status} {serial}: {partition}")
    return ok

def erase_partition(serial, partition):
    ok, msg = fastboot(f'erase {partition}', serial=serial)
    status = '✓' if ok else '✗'
    print(f"  {status} {serial}: erase {partition}")
    return ok

def reboot_mode(serial, mode='bootloader'):
    """bootloader, fastboot, recovery, system"""
    ok, _ = fastboot(f'reboot {mode}', serial=serial)
    return ok

def main():
    parser = argparse.ArgumentParser(description='Batch fastboot operations')
    parser.add_argument('--device', help='Single device serial')
    parser.add_argument('--batch', help='File with one serial per line')
    parser.add_argument('--flash-all', help='Directory with boot.img, system.img, vendor.img, etc.')
    parser.add_argument('--erase', help='Comma-separated partitions to erase')
    parser.add_argument('--reboot', choices=['bootloader','fastboot','recovery','system'], help='Reboot to mode')
    parser.add_argument('--parallel', type=int, default=2, help='Parallel devices')
    args = parser.parse_args()

    devices = []
    if args.device:
        devices = [args.device]
    elif args.batch:
        with open(args.batch) as f:
            devices = [l.strip() for l in f if l.strip()]
    else:
        devices = list_devices()
        if not devices:
            print("No fastboot devices found. Check: fastboot devices")
            sys.exit(1)

    print(f"\n🔧 Fastboot Batch — {len(devices)} device(s)\n")

    if args.flash_all:
        print(f"[FLASH] All from {args.flash_all}")
        images = glob.glob(f"{args.flash_all}/*.img")
        if not images:
            print(f"  No .img files found in {args.flash_all}")
            sys.exit(1)
        
        def flash_device(serial):
            for img_path in images:
                name = Path(img_path).stem
                flash_partition(serial, name, img_path)
        
        with ThreadPoolExecutor(max_workers=args.parallel) as ex:
            list(ex.map(flash_device, devices))

    elif args.erase:
        print(f"[ERASE] {args.erase}")
        partitions = args.erase.split(',')
        def erase_device(serial):
            for part in partitions:
                erase_partition(serial, part.strip())
        
        with ThreadPoolExecutor(max_workers=args.parallel) as ex:
            list(ex.map(erase_device, devices))

    elif args.reboot:
        print(f"[REBOOT] → {args.reboot}")
        with ThreadPoolExecutor(max_workers=args.parallel) as ex:
            for serial in devices:
                reboot_mode(serial, args.reboot)
                print(f"  ✓ {serial} → {args.reboot}")

    print("\n✅ Done.")

if __name__ == '__main__':
    main()
