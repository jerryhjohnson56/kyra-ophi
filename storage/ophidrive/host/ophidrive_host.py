#!/usr/bin/env python3
# ophidrive_host.py — vendor command helper (pyusb)
import usb.core, usb.util, sys, json

VENDOR_ID = 0x1209  # placeholder
PRODUCT_ID = 0x0F11 # placeholder
REQ_GET_MANIFEST = 0xA1
REQ_SET_PREFETCH = 0xB2

def find():
    return usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

def get_manifest(dev):
    try:
        data = dev.ctrl_transfer(0xC0, REQ_GET_MANIFEST, 0, 0, 4096)
        return json.loads(bytes(data).decode('utf-8', 'ignore'))
    except Exception as e:
        print("manifest error:", e)
        return None

def set_prefetch(dev, offsets):
    # offsets: list of uint64 offsets
    payload = b""
    for o in offsets:
        payload += int(o).to_bytes(8, 'little')
    try:
        dev.ctrl_transfer(0x40, REQ_SET_PREFETCH, 0, 0, payload)
        return True
    except Exception as e:
        print("prefetch error:", e); return False

if __name__ == "__main__":
    dev = find()
    if not dev:
        print("OphiDrive not found"); sys.exit(1)
    m = get_manifest(dev)
    print(json.dumps(m, indent=2))
    # set_prefetch(dev, [0, 65536, 131072])
