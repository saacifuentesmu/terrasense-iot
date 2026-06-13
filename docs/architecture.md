---
doc-id: TS-ARC-001
title: TerraSense IoT — System Architecture
version: "0.1"
status: draft
owner: Studio Lead
last-reviewed: 2026-06-12
---

# System Architecture (v0.1)

## 1. Overview

TerraSense IoT automates what is today a manual logging task in mushroom growing
rooms. Battery- or mains-powered sensor nodes measure temperature, humidity, and
(on at least one node) CO₂, report over a **Thread mesh** to a **border router**, which
hands telemetry to an **uplink bridge** that writes to **Firestore**. The existing
**TerraSense app** subscribes and shows live per-room readings, with manual entry
retained as fallback.

## 2. Block diagram

```
 ┌──────────────┐   Thread    ┌──────────────────┐   IP/Wi-Fi   ┌──────────────┐
 │ Sensor node  │  802.15.4   │  Border Router   │              │   Firestore  │
 │ nRF52840     │ ───────────▶│  Raspberry Pi    │ ────────────▶│  (cloud DB)  │
 │ SHT4x (+SCD41)│  CoAP/UDP  │  + nRF dongle RCP │   bridge     │              │
 │ Zephyr / NCS │            │  ot-br-posix      │ writes via   └──────┬───────┘
 └──────────────┘            │  + CoAP→FS bridge │ service acct        │ realtime
        ▲  ▲                 └──────────────────┘                      ▼
        │  └── mesh routing                                     ┌──────────────┐
 ┌──────────────┐                                               │ TerraSense   │
 │ Sensor node  │  (multi-hop to extend range across building)  │ app (Flutter)│
 └──────────────┘                                               └──────────────┘
```

## 3. Component choices

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Node MCU | **nRF52840** (DK now, module later) | Existing NCS/Zephyr expertise; mature Thread + BLE dynamic multiprotocol; strong low-power SED story. See [ADR-0001](decisions/0001-nrf-over-esp.md). |
| T/RH sensor | **SHT4x** (I²C) | Zephyr driver upstream; ±0.2 °C / ±1.8 %RH typical exceeds requirements. |
| CO₂ sensor | **SCD41** (I²C) | Photoacoustic NDIR, Zephyr driver; CO₂ drives fresh-air-exchange decisions in fruiting. |
| Border router | **Raspberry Pi + nRF52840 dongle (RCP)** running `ot-br-posix` | Reference, well-documented OTBR. The partner gateway can replace it later (GW-04). |
| Node ↔ BR transport | **CoAP over UDP** | Lightweight, REST-like, fits constrained nodes; clean confirmable messaging. |
| Uplink bridge | **Python service** (aiocoap server → Firestore Admin SDK) | Small, runs on the Pi; the documented seam for an external gateway. |
| Cloud | **Firestore** (existing) | App already reads it; realtime subscriptions; existing auth/rules. |
| App | **TerraSense** (existing, separate repo) | Reuse; add a live view. Decoupled via the data contract. |

## 4. Data path & the gateway seam

Nodes never talk to the cloud directly. They POST a small CoAP payload to the bridge;
the bridge maps it to the Firestore schema in [data-contract.md](data-contract.md) and
writes with the only cloud credentials in the system (GW-05). That payload format is the
**contract**: any gateway that produces it — including the coworkers' gateway product —
can replace the reference Pi bridge without touching firmware or app (GW-04). This is the
same ports-and-adapters discipline the app already uses for its backend.

## 5. Security model

- **Mesh:** commissioned Thread credentials (network key); no cleartext key in logs (SEC-01).
- **Cloud:** a scoped service account on the bridge; Firestore rules allow telemetry writes
  only from that identity; nodes and app hold no write creds (SEC-02, GW-05).
- **App:** existing authorized-account rules unchanged (SEC-03).

## 6. Time & idempotency

Nodes timestamp by uptime; the bridge reconciles to wall-clock on receipt (MEAS-04).
Writes are keyed by `node + timestamp` so retries can't duplicate samples (REL-03).

## 7. Phase plan (effort in weekend-blocks; ~10–12 h/week)

| Phase | Work | Exit gate |
|-------|------|-----------|
| **0 — Parallel start** | RTM, this doc, data contract; order hardware; stub app live view on fake data | Docs reviewed (C0/C1) |
| **1 — Node bring-up** | nRF52840 DK + SHT4x over I²C in Zephyr; RTT logging; no Thread yet | Reliable sensor reads |
| **2 — Thread up** | Pi OTBR running; node joins mesh; CoAP echo to bridge | Node ↔ BR round trip |
| **3 — Uplink** | CoAP server → Firestore writes | A reading lands in Firestore from the node |
| **4 — App live** | App subscribes to telemetry; add CO₂ node + 2nd node (mesh) | App shows two rooms updating live |
| **5 — Harden + polish** | Range/dropout/recovery tests; enclosure; demo script; **backup video** | Test report + RTM closed |

**Critical path:** order hardware in Phase 0 and do all paper + app-stub work while it
ships — import lead time is the top schedule risk, keep it off the critical path.

**Minimum viable demo:** 1 node (T/RH) → Thread → Pi BR → Firestore → live tile in the
app, plus the recorded video and the QMS docs. CO₂, 2nd-node mesh, battery SED, and a
custom PCB are stretch, in that order.
