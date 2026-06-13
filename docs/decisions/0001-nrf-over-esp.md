---
doc-id: TS-ADR-0001
title: ADR-0001 — nRF over ESP for sensor nodes
status: accepted
date: 2026-06-12
---

# ADR-0001 — nRF over ESP for sensor nodes

## Decision
Use **Nordic nRF52840** for the sensor nodes (dev kit now, module later), on
**nRF Connect SDK / Zephyr**.

## Context
Nodes need an 802.15.4 **Thread** radio, low power for battery operation, and ideally
**BLE** for local commissioning/config.

## Options
- **nRF52840 (chosen)** — Thread + BLE + low-power; mature OpenThread in NCS; reuses our
  existing BOMI NCS/Zephyr toolchain and experience.
- **ESP32 (classic)** — *cannot* do Thread (no 802.15.4 radio). Rejected.
- **ESP32-C6 / H2** — can do Thread, but the stack is newer/less proven and we'd learn
  ESP-IDF Thread from scratch. Kept in mind only for the partner **gateway** (its Wi-Fi
  makes a cheap integrated border router).

## Concurrent BLE + Thread
nRF52840/nRF5340 run **BLE and Thread concurrently** via *dynamic multiprotocol* — NCS's
MPSL time-slices the single radio. No button-switch needed; both stacks run at once.
Intended use: **BLE for commissioning/local config, Thread for telemetry** (NET-06,
a Could for v1).

## Consequences
- Lowest-risk path given existing expertise.
- nRF5340 is the drop-in upgrade if we later want Matter or more compute headroom.
- An nRF52840 USB dongle doubles as the border-router RCP.
