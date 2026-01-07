# Kyra Speed Stack PLUS — Direct I/O & GPUDirect (v1)
Generated: 2026-01-04T08:11:07.530638Z

This pack adds:
- **Direct I/O path** for model/page loads (io_uring/O_DIRECT on Linux, F_NOCACHE/mmap on macOS, DirectStorage on Windows).
- **GPUDirect Storage path** (NVMe→GPU DMA) when NVIDIA/cuFile is present.
- **Host/device vendor command reference for OphiDrive** (UASP + vendor ops).
- **Closed-loop auto‑tuner** that writes back per-box optimal **I/O schedulers, fan curves, CPU governors**.

## Support matrix (TL;DR)
| Platform | Direct I/O | GPUDirect/DirectStorage | Notes |
|---|---|---|---|
| Linux + NVIDIA | io_uring + O_DIRECT | **cuFile (GDS)** | Requires libcufile; NVMe & driver support. |
| Linux + AMD/Intel | io_uring + O_DIRECT | (N/A) | Normal DMA path; still benefits from Direct I/O. |
| macOS (Apple Silicon) | `mmap` + `F_NOCACHE` | (N/A) | Use Metal Heaps & shared memory hints. |
| Windows 11/Server | FileFlagNoBuffering | **DirectStorage** | Needs SDK; stub present. |

The local AIs will generate concrete backends behind traits. This kit provides **compilable stubs** and **examples**.
