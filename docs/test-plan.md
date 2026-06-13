---
doc-id: TS-TST-001
title: TerraSense IoT — Verification Test Plan
version: "0.1"
status: draft
owner: Studio Lead
last-reviewed: 2026-06-12
---

# Verification Test Plan (v0.1)

One procedure per testable requirement. Each run produces a dated record (pass/fail +
notes) that closes the matching RTM row. Stub — fill setup details as hardware lands.

## T-01 — Sensor accuracy (MEAS-01/02/03)
- **Setup:** node beside a reference thermo-hygrometer (and CO₂ reference for SCD41 node).
- **Steps:** log 30 min across two setpoints; compare node vs reference.
- **Pass:** |Δ| ≤ ±0.5 °C, ±3 %RH, ±(50 ppm + 5 %) CO₂.

## T-02 — Join time (NET-05)
- **Steps:** power-cycle node 10×; measure power-up → first telemetry in Firestore.
- **Pass:** ≤ 60 s every trial.

## T-03 — Range through wall (NET-03)
- **Steps:** node and parent separated through ≥ 1 interior wall; step distance to 15 m+;
  log RSSI / link quality and delivery ratio.
- **Pass:** link holds, delivery ≥ 99 % at 15 m / 1 wall.

## T-04 — Multi-hop routing (NET-04)
- **Steps:** place a node out of direct BR range, reachable only via a router node; confirm
  delivery and inspect route (≥ 2 hops).
- **Pass:** telemetry arrives via the intermediate hop.

## T-05 — Outage store-and-forward (GW-03, REL-02)
- **Steps:** disconnect bridge WAN for 2 h under normal sampling; restore; inspect Firestore.
- **Pass:** no samples lost within buffer window; series gap-free after flush.

## T-06 — Power-cycle recovery (REL-01)
- **Steps:** cut and restore node power unattended; observe rejoin + resumed sampling.
- **Pass:** auto-resumes with no manual action.

## T-07 — Idempotent writes (REL-03)
- **Steps:** force bridge retry of an already-written sample.
- **Pass:** no duplicate/corrupted doc (same `epochSec` key overwrites cleanly).

## T-08 — End-to-end latency & stale flag (APP-01/02)
- **Steps:** time sample → app render; then stop a node and watch the stale indicator.
- **Pass:** ≤ 10 s to render; stale flag after > 2 intervals.

## T-09 — Battery life (PWR-01) — analysis then measurement
- **Analysis:** current profile (sleep + TX) → projected months on 2×AA at 5-min interval.
- **Measurement:** power-profiler average current over a representative window.
- **Pass:** projection ≥ 6 months; measured average within budget.

## T-10 — Security inspection (SEC-01/02, GW-05)
- **Checks:** no Thread key in logs; only bridge service account can write; rules reject
  unauthenticated/node writes; app limited to authorized accounts.
- **Pass:** all checks hold.
