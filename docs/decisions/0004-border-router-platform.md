---
doc-id: TS-ADR-0004
title: ADR-0004 — Raspberry Pi + nRF52840 RCP as border router
status: accepted
date: 2026-07-12
---

# ADR-0004 — Raspberry Pi + nRF52840 RCP as border router

## Decision
Run the PoC border router on a **Raspberry Pi + nRF52840 dongle (RCP)** with
**`ot-br-posix`**, as already sketched in [architecture.md](../architecture.md).
**BeaglePlay is the documented fallback** if the Pi/dongle path stalls.

## Context
Both platforms are on hand, so stock and price are moot. The PoC optimizes for
time-to-demo; the production border router is the partner gateway behind the
bridge seam (GW-04), so PoC robustness is not a driver.

## Options
- **Raspberry Pi + nRF52840 RCP (chosen)** — the canonical OTBR reference platform;
  OpenThread's and Nordic's guides document exactly this setup. Same vendor as the
  node (NCS/Zephyr both sides) keeps any Thread debugging single-stack.
- **BeaglePlay** — official OpenThread BR image on the onboard CC1352; integrated
  radio and eMMC make it the more robust box. Rejected for the PoC: much smaller
  community, and a TI↔Nordic cross-vendor mesh is slower to debug under a deadline.
- **STM32MP2 / other Linux DKs** — no maintained OTBR path; would be porting work
  with zero PoC value. Rejected.

## Consequences
- Phase 2 bring-up: flash the dongle as RCP, install `ot-br-posix` on the Pi — runbook
  in [gateway/otbr-setup.md](../../gateway/otbr-setup.md).
- If cross-cutting Pi issues burn more than a day, switch to BeaglePlay and record
  the switch here.
