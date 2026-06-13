# TerraSense IoT

Automated Thread-based environmental monitoring for mushroom growing rooms ("Iglús").
Replaces manual logging with a wireless sensor mesh that feeds the existing
TerraSense companion app.

Part of **Seekio Labs**. This repo is the **device system** — sensor nodes, gateway,
hardware, and project docs. The companion app lives in its own repo (`terrasense`);
see [ADR-0002](docs/decisions/0002-repo-topology.md) for why they are split.

## System at a glance

```
[Sensor nodes]        [Border Router]         [Uplink bridge]      [Cloud]      [App]
 nRF52840 + SHT4x  →   Pi + nRF dongle    →    CoAP → Firestore  →  Firestore →  TerraSense
 (+ SCD41 CO2)         ot-br-posix (RCP)       (Python service)                  (live view)
 Zephyr / NCS          Thread → IP
 Thread mesh
```

## Layout

| Dir | Contents |
|-----|----------|
| `docs/` | RTM, architecture, data contract, test plan, decision records |
| `firmware/` | Sensor node firmware (nRF Connect SDK / Zephyr) |
| `gateway/` | Border-router config + CoAP→Firestore uplink bridge |
| `hardware/` | Schematics, BOM, board files (dev kits now, custom boards later) |

## Status

**Phase 0 — scoping.** Start at [docs/RTM.md](docs/RTM.md), then
[docs/architecture.md](docs/architecture.md). Phase plan lives in the architecture doc.
