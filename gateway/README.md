# gateway

Thread Border Router + uplink bridge.

## Parts
- **Border router:** Raspberry Pi 4 + nRF52840 dongle PCA10059 (RCP) running `ot-br-posix`
  — bring-up runbook: [otbr-setup.md](otbr-setup.md).
- **Uplink bridge:** Python service — CoAP server (aiocoap) that maps node payloads to the
  Firestore schema and writes via a scoped service account.

## Contract
The bridge implements [../docs/data-contract.md](../docs/data-contract.md). Any gateway
that emits the same cloud schema (incl. the partner gateway) can replace this one (GW-04).

## Security
The service-account JSON is the **only** cloud credential in the system (GW-05). Keep it out
of git (already in `.gitignore`); store under `gateway/` locally as `service-account.json`.

## Run
```
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python -m bridge --dry-run          # no cloud; logs writes in memory
python -m bridge --credentials service-account.json   # real Firestore
```

## Simulated node (Phase 0)
Stands in for the nRF52840 node until firmware lands — proves bridge, schema, and
app live-tile end to end with no hardware:
```
python tools/simnode.py --node iglu_1 --interval 5
```

## Tests
```
pip install -r requirements-dev.txt
ruff check . && pytest
```
