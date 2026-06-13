---
doc-id: TS-ADR-0002
title: ADR-0002 — Repository topology
status: accepted
date: 2026-06-12
---

# ADR-0002 — Repository topology

## Decision
**Device-system monorepo** (`terrasense-iot`: firmware + gateway + hardware + docs) and a
**separate app repo** (`terrasense`). The two are joined by the documented
[data contract](../data-contract.md), not by code.

## Context
The system spans Zephyr firmware, a Python bridge, KiCad hardware, and a Flutter app —
different toolchains, CI, and release cadences. The app is also a *reusable* companion-app
template, not specific to this one product, and already lives in its own repo.

## Options
- **One mega-repo (all four layers).** Simplest single RTM, atomic cross-cutting changes —
  but couples the reusable app to one product and bloats CI with four toolchains. Rejected.
- **Device monorepo + separate app (chosen).** Firmware/gateway/hardware/docs evolve and
  trace together (one RTM); the app stays reusable; the data contract is the seam.
- **A repo per component (firmware, gateway, hw, app).** Maximum decoupling, but scatters
  the RTM and makes traceability painful for a solo founder. Rejected for now.

## Consequences
- Project technical records (RTM, architecture, test reports) live **in this repo's `docs/`**,
  version-controlled with the code — git is the audit trail, per the Seekio QMS.
- `seekio-internal` holds process **templates**; this repo holds the **filled-in records**.
- The firmware↔app interface is governed by `docs/data-contract.md`; either side can change
  independently as long as the contract holds.
