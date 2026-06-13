---
doc-id: TS-ADR-0003
title: ADR-0003 — Dev kits now, custom boards later
status: accepted
date: 2026-06-12
---

# ADR-0003 — Dev kits now, custom boards later

## Decision
Build on **nRF52840 dev kits** for the demo, then migrate to a **module-based custom board**
as the project matures. Keep firmware **board-abstracted** from day one so the move is a
board-definition change, not a rewrite (PROC-03).

## Context
Dev kits get us to a working demo fastest. Production needs a small, enclosed, possibly
battery node. We want to pay the custom-board cost only once value is proven, without a
firmware rewrite when we do.

## How we keep migration cheap
- All pin/peripheral assignments live in **Zephyr devicetree** (`boards/` overlays), never
  hardcoded in C. Dev kit and custom board are two board definitions over the same app.
- Prefer a **pre-certified nRF52840 module** (e.g. Raytac MDBT50Q, Fanstel BT840) over bare
  silicon — saves RF layout and gets modular FCC/CE, consistent with the service catalog's
  "pre-certified modules" stance.
- Sensors stay on I²C with upstream Zephyr drivers, so the custom board reuses the same
  driver bring-up.

## Consequences
- Custom PCB is a **stretch** item (after the demo), not on the critical path.
- The hardware effort becomes: module + sensors + power + enclosure, with firmware already
  proven on the DK.
- A new `boards/` entry + a build-and-flash pass is the bulk of the migration.
