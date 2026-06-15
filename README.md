# TerraSense IoT

Automated Thread-based environmental monitoring for mushroom growing rooms ("Iglús").
Replaces hand-written temperature/humidity logs with a wireless sensor mesh that feeds
a Flutter companion app in real time.

A working environmental-monitoring system I'm designing and building end-to-end —
firmware, mesh networking, cloud uplink, and app — against a real growing facility.
Part of **Seekio Labs**.

## The problem

The rooms are logged by hand: someone walks each Iglú, reads a thermo-hygrometer, and
writes it on paper. It's sparse, error-prone, and there's no alarm when a room drifts
out of range overnight — exactly when a crop is lost. TerraSense makes the readings
continuous, wireless, and visible from a phone.

## System at a glance

```
[Sensor nodes]        [Border Router]         [Uplink bridge]      [Cloud]      [App]
 nRF52840 + SHT4x  →   Pi + nRF dongle    →    CoAP → Firestore  →  Firestore →  TerraSense
 (+ SCD41 CO2)         ot-br-posix (RCP)       (Python service)                  (live view)
 Zephyr / NCS          Thread → IP
 Thread mesh
```

Battery sensor nodes form a self-healing **Thread** mesh and push readings over **CoAP**
to a Raspberry Pi border router. A small Python bridge translates CoAP → Firestore in a
fixed [data contract](docs/data-contract.md), and the [companion app](#companion-app)
renders a live per-room view with a stale-data flag.

## Engineering decisions

The reasoning behind the stack lives in [Architecture Decision Records](docs/decisions/):

| Decision | Why | ADR |
|----------|-----|-----|
| **nRF52840 over ESP32** | Mesh scalability + sub-µA sleep for battery nodes; Thread/802.15.4 radio | [0001](docs/decisions/0001-nrf-over-esp.md) |
| **Device system split from the app** | Firmware and app evolve independently behind a versioned data contract | [0002](docs/decisions/0002-repo-topology.md) |
| **Dev kits now, custom board later** | De-risk firmware/protocol before committing to a PCB spin | [0003](docs/decisions/0003-devkit-to-custom-board.md) |
| **Thread mesh + BLE multiprotocol** | Mesh range across concrete rooms; BLE kept for local provisioning | [architecture.md](docs/architecture.md) |
| **Data contract as the seam** | Any gateway emitting the schema can replace the reference bridge | [data-contract.md](docs/data-contract.md) |

## What it demonstrates

End-to-end embedded product work: low-power nRF/Zephyr firmware, Thread mesh +
CoAP/UDP, BLE/Thread dynamic multiprotocol, a border-router uplink, and a clean
firmware↔app decoupling driven by requirements traceability (two RTMs) and ADRs —
not just a wired-up demo.

## Layout

| Dir | Contents |
|-----|----------|
| `docs/` | RTM (PoC + system), architecture, data contract, test plan, decision records |
| `firmware/` | Sensor node firmware (nRF Connect SDK / Zephyr) |
| `gateway/` | Border-router config + CoAP→Firestore uplink bridge |
| `hardware/` | Schematics, BOM, board files (dev kits now, custom boards later) |

## Companion app

The phone app lives in its own repo (sanitized public build). It's a Flutter +
Riverpod + Firebase client with a ports-and-adapters backend (Firestore/REST
interchangeable), offline-first sync, and EN/ES localization.

## Status

**Phase 0 — scoping.** Two requirements-traceability matrices drive the build:
[docs/RTM-poc.md](docs/RTM-poc.md) is the de-risking + demo scope;
[docs/RTM-system.md](docs/RTM-system.md) is the production target. Passing the PoC
baselines the system RTM. See [docs/architecture.md](docs/architecture.md) for the
phase plan.
