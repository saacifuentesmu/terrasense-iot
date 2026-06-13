---
doc-id: TS-RTM-001
title: TerraSense IoT — Requirements & Traceability Matrix
version: "0.1"
status: draft
owner: Studio Lead
last-reviewed: 2026-06-12
---

# Requirements & Traceability Matrix (RTM v0.1)

## Purpose & scope

Defines the requirements for **TerraSense IoT**: a Thread-based wireless sensor
system that automates environmental monitoring of mushroom growing rooms ("Iglús"),
replacing today's manual readings and feeding the existing TerraSense app.

Scope: sensor nodes, Thread mesh, border router + uplink bridge, and the cloud data
contract the app consumes. **Monitoring only — no actuation/climate control in v1.**

> This is a draft for review. Numbers in *italics* are proposals to confirm — see
> [Open questions](#open-questions). Trace and Status columns are filled in as the
> design progresses (the "living" part of the RTM).

**Legend** — Priority: **M**ust / **S**hould / **C**ould (MoSCoW).
Verify: **T**est / **D**emonstration / **I**nspection / **A**nalysis.
Status: Open → Designed → Verified.

## MEAS — Measurement

| ID | Requirement | Pri | Verify | Trace | Status |
|----|-------------|-----|--------|-------|--------|
| MEAS-01 | Each node shall measure air temperature *0–50 °C* with accuracy ≤ *±0.5 °C* | M | T | — | Open |
| MEAS-02 | Each node shall measure relative humidity *0–100 %RH* with accuracy ≤ *±3 %RH* | M | T | — | Open |
| MEAS-03 | At least one node shall measure CO₂ *400–5000 ppm* with accuracy ≤ *±(50 ppm + 5 %)* | S | T | — | Open |
| MEAS-04 | Each sample shall carry a timestamp (node uptime reconciled to wall-clock at the gateway) | M | I | — | Open |
| MEAS-05 | Sampling interval shall be configurable *1–15 min* (default *5 min*); demo profile *30 s* | M | D | — | Open |

## NET — Thread network

| ID | Requirement | Pri | Verify | Trace | Status |
|----|-------------|-----|--------|-------|--------|
| NET-01 | Nodes shall communicate over an 802.15.4 Thread mesh | M | D | — | Open |
| NET-02 | System shall support *≥ 9* monitored rooms (Iglú 1–9) on one mesh | M | T | — | Open |
| NET-03 | A node-to-node link shall hold through *≥ 1 interior wall at ≥ 15 m* | S | T | — | Open |
| NET-04 | Mesh shall route multi-hop (*≥ 2 hops*) to reach the border router | S | T | — | Open |
| NET-05 | A node shall (re)join the Thread network within *60 s* of power-up | M | T | — | Open |
| NET-06 | Node shall support BLE local commissioning/config concurrently with Thread (dynamic multiprotocol) | C | D | — | Open |

## GW — Gateway & uplink

| ID | Requirement | Pri | Verify | Trace | Status |
|----|-------------|-----|--------|-------|--------|
| GW-01 | A Thread Border Router shall bridge the mesh to IP | M | D | — | Open |
| GW-02 | Node telemetry shall be delivered to the cloud datastore (Firestore) via the uplink bridge | M | T | — | Open |
| GW-03 | The bridge shall store-and-forward telemetry for *≥ 2 h* during a cloud/WAN outage and flush on recovery | M | T | — | Open |
| GW-04 | The uplink interface shall be a documented contract so an external (partner) gateway can replace the reference bridge | S | I | data-contract.md | Open |
| GW-05 | Only the bridge service account shall hold cloud write credentials; nodes hold none | M | I | — | Open |

## APP — Application (existing TerraSense app)

| ID | Requirement | Pri | Verify | Trace | Status |
|----|-------------|-----|--------|-------|--------|
| APP-01 | App shall display the latest reading per room within *10 s* of a sample reaching the cloud | M | D | — | Open |
| APP-02 | App shall flag stale data when no sample is received for *> 2 sampling intervals* | M | T | — | Open |
| APP-03 | Existing manual data entry shall remain available as a fallback | M | D | exists | Open |
| APP-04 | App shall show recent history/trend per room and metric | S | D | — | Open |
| APP-05 | App shall remain offline-first per the existing sync design | M | D | exists | Open |

## PWR — Power

| ID | Requirement | Pri | Verify | Trace | Status |
|----|-------------|-----|--------|-------|--------|
| PWR-01 | Battery nodes (Sleepy End Device) shall last *≥ 6 months* on *2×AA* at 5-min interval | S | A→T | — | Open |
| PWR-02 | A mains/USB-powered node profile shall be supported for the v1 demo | M | D | — | Open |

## ENV — Environmental

| ID | Requirement | Pri | Verify | Trace | Status |
|----|-------------|-----|--------|-------|--------|
| ENV-01 | Node shall operate 0–50 °C and up to *95 %RH* with electronics protected from condensation | M | A/I | — | Open |
| ENV-02 | Sensor opening shall use a hydrophobic (e.g. PTFE) membrane to survive high-humidity rooms | S | I | — | Open |

## REL — Reliability

| ID | Requirement | Pri | Verify | Trace | Status |
|----|-------------|-----|--------|-------|--------|
| REL-01 | A node shall auto-resume (rejoin + resume sampling) after a power cycle, unattended | M | T | — | Open |
| REL-02 | The bridge shall auto-resume uploads after WAN restoration with no loss within the buffer window | M | T | — | Open |
| REL-03 | Writes shall be idempotent (keyed by node + timestamp) so a retry cannot duplicate or corrupt the series | S | I | data-contract.md | Open |

## SEC — Security

| ID | Requirement | Pri | Verify | Trace | Status |
|----|-------------|-----|--------|-------|--------|
| SEC-01 | Thread mesh shall use commissioned credentials (network key); keys shall not appear in cleartext logs | M | I | — | Open |
| SEC-02 | Cloud writes shall be authenticated via a scoped service account; rules restrict writes to the bridge identity | M | I/T | — | Open |
| SEC-03 | App access shall stay restricted to authorized accounts per existing Firestore rules | S | D | exists | Open |

## PROC — Process / non-functional

| ID | Requirement | Pri | Verify | Trace | Status |
|----|-------------|-----|--------|-------|--------|
| PROC-01 | Firmware shall build in CI and pass static analysis before merge | M | I | — | Open |
| PROC-02 | Each requirement shall trace to a design element, implementation, and verification record before design freeze (C3) | M | I | this doc | Open |
| PROC-03 | Firmware shall be board-abstracted so a dev-kit → custom-board move is a board-definition change, not a rewrite | S | I | [ADR-0003](decisions/0003-devkit-to-custom-board.md) | Open |

## Open questions

Confirm or correct these before the matrix is baselined to v1.0:

1. **Rooms / nodes for the demo** — 9 to match the app, or fewer (e.g. 2–3) for the first demo with the schema sized for 9?
2. **CO₂** — one node, or all? (SCD41 is the costliest sensor; one CO₂ node + several T/RH nodes is the sensible split.)
3. **Power for v1** — mains/USB nodes (simpler) or battery SED from the start? (Proposal: mains for v1 demo, SED as a stretch — PWR-01 stays Should.)
4. **Sampling interval** — confirm production default (proposed 5 min) and demo profile (proposed 30 s).
5. **History retention** — how long do per-room samples live in Firestore? Drives cost and the APP-04 trend view.
6. **Actuation** — confirmed out of scope for v1 (monitoring only)? Climate control would be a later phase.
