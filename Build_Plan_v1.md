
# OphiBox Overlays — Build Plan (v1)
Generated: 2026-01-04T09:22:32.661732Z

## Complexity — honest assessment
- **Hardware**: Moderate-high (HDMI 2.0 pass-through + capture + low-latency overlay). Feasible with off‑the‑shelf SoMs and HDMI Rx/Tx bridge chips. Biggest risks: HDCP handling, signal integrity, thermals.
- **Software**: Moderate (Month 1–3 MVP) → High (V2 AI triggers, pro features). GStreamer/FFmpeg pipelines, WASM overlay runtime, OCR/ASR small models.
- **Manufacturing**: Moderate (small-run boxes). Certification adds time and cost.

## Phased Timeline (aggressive but doable)
- **Phase 0 (2–3 weeks)**: Dev board bring-up (RK3588 or Orin), USB capture mock → overlay → HDMI out. Overlay packs + editor prototype.
- **Phase 1 (6–8 weeks)**: Custom board EVT (HDMI Rx/Tx + SoM), Linux image, GStreamer pipeline, single overlay plane @ 4K60 pass-through, 1080p60 encode. Online vs SP profiles.
- **Phase 2 (6–10 weeks)**: Linter + pack format, AI triggers (VAD/ASR/OCR), clip buffer, templates, OphiCache integration, recovery.
- **Phase 3 (cert + DVT/PVT, 8–12 weeks)**: Thermal tuning, acoustics, CE/FCC, packaging, docs, localized installer.

## Team (lean)
- **1 HW lead** (schematic/PCB/bring-up), **1 FW/driver**, **2 video/graphics/overlay**, **1 CV/ASR**, **1 web/UX**, **1 QA/Release**.
- With your local AIs coding, human leads mostly review/merge/drive integration.

## BOM Snapshot (prototype → low volume)
- **Base (RK3588)**: BOM ≈ **$233.1**, COGS est ≈ **$291.38**, MSRP target ≈ **$372.96**.
- **Pro (Orin)**: BOM ≈ **$354.1**, COGS est ≈ **$442.62**, MSRP target ≈ **$566.56**.

\* Licensing: HDMI/HDCP costs vary by program and volume; per‑unit amortization here is a placeholder. You’ll also budget for CE/FCC testing, packaging, and logistics.

## Major Risks & Mitigations
- **HDCP/ToS**: Pass-through must be compliant; gameplay capture typically allowed when consoles disable HDCP for games—OS apps remain protected. Mitigation: honor HDCP signals; disable capture path automatically; overlays remain permitted for non-protected modes.
- **Latency budget**: Keep end‑to‑end added latency < 16ms. Mitigation: zero-copy DMA‑BUF, single overlay plane, fixed pipeline, precompiled shaders.
- **Thermals/acoustics**: Active cooling tuned by MCU; target < 28 dBA typical.
- **Supply chain**: Dual-source HDMI bridges; SoM option for fast spin; enclosure vendor backup.
- **AI on device**: Start with small models (VAD/ASR/OCR) and offload heavier features to PC when available; later add OphiAccel.

## What ships in MVP
- 4K60 HDR pass‑through, 1080p60 encode/stream, single overlay plane.
- Layout Editor + 6 starter templates, overlay pack format + linter.
- Local captions/translation, FPS/frametime graphs, timers/splits, chat widgets.
- SP/Co‑op vs Online profiles (safe by default), recovery image, logs/metrics.
