# OphiDrive Vendor Commands (Device Side Outline)
USB: UASP Mass Storage (BotAlt) with vendor control requests

Requests:
- **0xA1 GET_MANIFEST** — Returns JSON: name -> sha256 -> offset/length
- **0xB2 SET_PREFETCH** — Body: array of 64-bit offsets (hot pages) for DRAM prefetch

Implementation:
- On GET_MANIFEST, dump current layout of /KPACK/
- On SET_PREFETCH, schedule read-ahead from NVMe -> DRAM window

Safety:
- Ignore invalid offsets; cap prefetch budget; watchdog resets window per LRU.
