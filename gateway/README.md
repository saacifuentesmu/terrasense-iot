# gateway

Thread Border Router + uplink bridge.

## Parts
- **Border router:** Raspberry Pi + nRF52840 dongle (RCP) running `ot-br-posix`.
- **Uplink bridge:** Python service — CoAP server (aiocoap) that maps node payloads to the
  Firestore schema and writes via a scoped service account.

## Contract
The bridge implements [../docs/data-contract.md](../docs/data-contract.md). Any gateway
that emits the same cloud schema (incl. the partner gateway) can replace this one (GW-04).

## Security
The service-account JSON is the **only** cloud credential in the system (GW-05). Keep it out
of git (already in `.gitignore`); store under `gateway/` locally as `service-account.json`.

## Run (to fill in Phase 3)
```
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python bridge.py
```
