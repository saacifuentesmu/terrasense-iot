---
doc-id: TS-DAT-001
title: TerraSense IoT — Data Contract (node ↔ bridge ↔ cloud ↔ app)
version: "0.1"
status: draft
owner: Studio Lead
last-reviewed: 2026-06-12
---

# Data Contract (v0.1)

The interface that keeps firmware and app decoupled (GW-04, REL-03). Any gateway that
emits the cloud schema below can replace the reference bridge. **Proposal for review —
align field names with the app before baselining.**

## 1. Node → bridge (CoAP)

`POST coap://<bridge>/telemetry` — payload CBOR (preferred) or JSON:

```json
{
  "node": "iglu_1",        // room/node id, matches app deviceId(i) = "iglu_$i"
  "fw":   "0.1.0",
  "seq":  1423,             // monotonic per node; dedupe + loss detection
  "up_ms": 73512000,        // node uptime at sample (bridge reconciles to wall-clock)
  "t":    21.4,             // °C
  "rh":   88.2,             // %RH
  "co2":  920,              // ppm, omit on non-CO2 nodes
  "batt": 2960              // mV, omit on mains nodes
}
```

Confirmable CoAP; node retries until ACK or buffer-full (NET/REL requirements).

## 2. Cloud schema (Firestore)

Reuses the app's existing `igloos` collection and `meta/latest` fast-start pattern.

**Latest reading per room** — `igloos/{node}` document, `live` map:

```
igloos/iglu_1
  live: { t: 21.4, rh: 88.2, co2: 920, batt: 2960,
          ts: <serverTimestamp>, seq: 1423, source: "thread" }
```

**History** — `igloos/{node}/samples/{epochSec}` (doc id = unix seconds → idempotent, REL-03):

```
igloos/iglu_1/samples/1749700800
  { t: 21.4, rh: 88.2, co2: 920, ts: 1749700800 }
```

**Startup summary** — `meta/latest` updated on each write so the app does 1 read at launch
(matches the existing sync design):

```
meta/latest
  rooms: { iglu_1: {t,rh,co2,ts}, iglu_2: {...}, ... }
  updated: <serverTimestamp>
```

## 3. App consumption

- **Live view:** subscribe to `meta/latest` (or per-room `igloos/{id}.live`); render latest
  per room; flag stale when `now - ts > 2 × interval` (APP-01, APP-02).
- **History/trend:** query `igloos/{id}/samples` over a time window (APP-04).
- **Fallback:** manual entry writes the same shape with `source: "manual"` (APP-03).

## 4. Units & ranges (authoritative)

| Field | Unit | Range | Note |
|-------|------|-------|------|
| `t` | °C | 0–50 | MEAS-01 |
| `rh` | %RH | 0–100 | MEAS-02 |
| `co2` | ppm | 400–5000 | MEAS-03, optional |
| `batt` | mV | 0–3600 | optional, SED only |
| `ts` | unix s | — | wall-clock, bridge-assigned |
| `seq` | int | monotonic/node | loss + dedupe |

## 5. Open

- Confirm field names against the app's existing model / CSV vocabulary (`T Sala`, etc.).
- Decide history retention (drives `samples` TTL / cost) — see RTM open question 5.
