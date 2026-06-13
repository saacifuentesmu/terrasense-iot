---
doc-id: TS-NOTE-001
title: TerraSense IoT — App Live-View Stub (Phase 0 implementation note)
version: "0.1"
status: draft
owner: Studio Lead
last-reviewed: 2026-06-13
---

# App live-view stub — implementation note

Phase 0, hardware-independent. De-risks **POC-08** (app renders a live tile) and **POC-09**
(stale flag) before any node exists, by driving the app from a fake Firestore writer. When a
real reading later lands via the bridge, the app already shows it. Lives in the `terrasense`
app repo; this note is the brief.

## Goal

A live per-room tile in the TerraSense app showing latest T/RH (later CO₂), subscribed to
Firestore per [data-contract.md](data-contract.md), updating in real time, flagging stale data.
No hardware, no firmware — a fake writer stands in for the node→bridge path.

## Blocker to resolve first — doc-id mismatch

The data contract assumes `igloos/{node}` keyed by `node = "iglu_1"` (`deviceId`), but the app
today keys that collection by **display name**: `FirebaseDataStore` calls
`.collection('igloos').doc(deviceName)` where `deviceName = "Iglú 1"`
([firebase_data_store.dart](../../terrasense-sample/lib/core/backend/adapters/firebase_data_store.dart),
`AppConstants.deviceName(i)`). So `iglu_1` and `Iglú 1` are different documents.

Pick one before writing anything:
- **(A, recommended)** Telemetry lives in its own doc keyed by `deviceId` (`iglu_1`) — e.g. a
  separate `telemetry/{deviceId}` doc or the `live` map under an `iglu_1`-keyed doc — and the
  app maps `deviceId(i)` → tile. Keeps the existing accented-name `igloos/{deviceName}` cycle
  docs untouched; no migration. Cleanest seam.
- **(B)** Re-key the `igloos` collection by `deviceId` and migrate existing cycle docs. Tidier
  long-term, but touches working data and the storage path. Out of scope for the PoC.

Decision updates the data contract's §2 before baselining.

## Work (in the app repo)

1. **Telemetry port** — new `TelemetryStore` port (ports-and-adapters, mirrors `DataStore`):
   `Stream<Map<String, LiveReading>> watchLive()` and/or
   `Stream<LiveReading> watchRoom(String deviceId)`. Domain-shaped, no `cloud_firestore` import.
2. **Model** — `LiveReading` (Freezed): `t`, `rh`, `co2?`, `batt?`, `ts` (DateTime), `seq`,
   `source`. Mirror data-contract §2 field names exactly.
3. **Firebase adapter** — `FirebaseTelemetryStore` implements the port via a Firestore
   `snapshots()` subscription on the chosen doc/collection (per blocker decision). Only file
   that imports `cloud_firestore` for telemetry.
4. **Provider** — Riverpod `StreamProvider` over the port; tile widget on the device list /
   detail screen. Stale rule: `now - ts > 2 × interval` → stale badge (APP-02 / POC-09).
5. **Fake writer (the stub)** — a small standalone Dart script *or* an `InMemoryTelemetryStore`
   adapter that emits a sine-ish T/RH every ~30 s. Two flavors, pick per goal:
   - in-app fake adapter (no Firestore) — fastest to see the UI move; or
   - a `tools/fake_telemetry.dart` that writes real Firestore docs in the contract shape —
     also exercises the adapter + rules end to end (closer to POC-08). Prefer this one.

## Done when

- Tile renders latest T/RH for ≥1 room and updates live as the fake writer ticks.
- Stale badge appears when the writer stops for > 2× interval.
- `cloud_firestore` confined to the telemetry adapter (port discipline intact).
- Data contract §2 updated with the resolved doc-id decision.

## Deferred (not this stub)

CO₂ tile rendering polish, history/trend charts (APP-04), manual-entry `source: "manual"`
path (APP-03) — already in the system RTM.
