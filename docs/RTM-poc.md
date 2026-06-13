---
doc-id: TS-RTM-POC-001
title: TerraSense IoT — PoC Requirements & Traceability Matrix
version: "0.1"
status: draft
owner: Studio Lead
last-reviewed: 2026-06-12
---

# PoC RTM (v0.1)

## PoC question

> **Can a Thread sensor node deliver a live reading into the TerraSense app, end to end
> (node → border router → Firestore → app)?**

This is the de-risking + recruiter-demo scope — prove the integration path works, not the
production targets. The full production requirements live in
[RTM-system.md](RTM-system.md); each PoC row links to the system requirement it previews.

Scope: **one mains-powered T/RH node, single-hop Thread, one live room tile in the app,
plus a recorded video and a PoC summary.** Everything else is deferred (see
[Deferred](#deferred-to-the-system-rtm)).

**Legend** — Priority **M**/**S**/**C**; Verify **T**/**D**/**I**/**A**; Status Open → Done.

## Requirements

| ID | Requirement | Pri | Verify | Previews | Status |
|----|-------------|-----|--------|----------|--------|
| POC-01 | Node measures temperature + humidity via SHT4x over I²C | M | D | MEAS-01/02 | Open |
| POC-02 | Node samples on a fixed demo interval (~30 s) | M | D | MEAS-05 | Open |
| POC-03 | Node joins a Thread network and reaches the border router (single hop is fine) | M | D | NET-01/05 | Open |
| POC-04 | Node reports each reading to the bridge over CoAP | M | D | GW-02 | Open |
| POC-05 | Raspberry Pi border router (`ot-br-posix`) bridges Thread ↔ IP | M | D | GW-01 | Open |
| POC-06 | Bridge writes each reading to Firestore per the data contract | M | D/T | GW-02 | Open |
| POC-07 | Only the bridge holds cloud write credentials; the node holds none | S | I | GW-05, SEC-02 | Open |
| POC-08 | App shows the node's latest T/RH as a live room tile, updating within ~10 s | M | D | APP-01 | Open |
| POC-09 | App flags stale data if the node stops reporting | S | D | APP-02 | Open |
| POC-10 | A recorded demo video captures the end-to-end path (interview-safe backup) | M | I | — | Open |
| POC-11 | A 1–2 page PoC Summary is produced (objective, setup, observations, risks, next steps) | M | I | service catalog `PoC1D` | Open |

## Deferred to the system RTM

Out of scope for the PoC — these are where the real engineering happens and stay in
[RTM-system.md](RTM-system.md):

| Deferred | System req |
|----------|------------|
| CO₂ sensing (SCD41) | MEAS-03 |
| ≥ 9 rooms on one mesh | NET-02 |
| Range-through-wall + multi-hop | NET-03, NET-04 |
| BLE commissioning (multiprotocol) | NET-06 |
| 2 h store-and-forward on outage | GW-03 |
| Strict idempotency / loss guarantees | REL-03 |
| Unattended power-cycle recovery (formal test) | REL-01 |
| Battery / Sleepy End Device + life target | PWR-01 |
| Enclosure + PTFE membrane for 95 %RH | ENV-01/02 |
| CI build + static-analysis gate | PROC-01 |
| Formal security verification | SEC-01, SEC-02 |

## Exit

PoC passes when POC-01..06, POC-08, POC-10, POC-11 are **Done** (the Musts). Passing the PoC
is the C1 trigger to baseline [RTM-system.md](RTM-system.md) to v1.0 and plan the build-out.
