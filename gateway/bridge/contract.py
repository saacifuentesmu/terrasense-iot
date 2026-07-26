"""Payload validation and cloud-schema mapping per docs/data-contract.md (TS-DAT-001 v0.1)."""

import json
import time
from dataclasses import dataclass

import cbor2


class ContractError(ValueError):
    """Payload violates the data contract."""


REQUIRED = ("node", "fw", "seq", "up_ms", "t", "rh")
OPTIONAL = ("co2", "batt")
RANGES = {"t": (0, 50), "rh": (0, 100), "co2": (400, 5000), "batt": (0, 3600)}


@dataclass(frozen=True)
class Reading:
    node: str
    fw: str
    seq: int
    up_ms: int
    t: float
    rh: float
    co2: int | None = None
    batt: int | None = None
    ts: int = 0  # wall-clock unix seconds, bridge-assigned (contract §4)


def parse(payload: bytes, now=time.time) -> Reading:
    """Decode a node telemetry payload (CBOR preferred, JSON fallback) and validate it."""
    try:
        data = cbor2.loads(payload)
    except Exception:
        try:
            data = json.loads(payload)
        except Exception:
            raise ContractError("payload is neither valid CBOR nor JSON") from None
    if not isinstance(data, dict):
        raise ContractError("payload must be a map")

    missing = [k for k in REQUIRED if k not in data]
    if missing:
        raise ContractError(f"missing fields: {missing}")
    unknown = sorted(set(data) - set(REQUIRED) - set(OPTIONAL))
    if unknown:
        raise ContractError(f"unknown fields: {unknown}")

    if not isinstance(data["node"], str) or not data["node"]:
        raise ContractError("node must be a non-empty string")
    if not isinstance(data["fw"], str):
        raise ContractError("fw must be a string")
    for k in ("seq", "up_ms"):
        if not isinstance(data[k], int) or data[k] < 0:
            raise ContractError(f"{k} must be a non-negative integer")
    for k, (lo, hi) in RANGES.items():
        v = data.get(k)
        if v is None:
            continue
        if isinstance(v, bool) or not isinstance(v, (int, float)) or not lo <= v <= hi:
            raise ContractError(f"{k}={v!r} outside contract range [{lo}, {hi}]")

    return Reading(
        node=data["node"],
        fw=data["fw"],
        seq=data["seq"],
        up_ms=data["up_ms"],
        t=float(data["t"]),
        rh=float(data["rh"]),
        co2=data.get("co2"),
        batt=data.get("batt"),
        ts=int(now()),
    )


# Cloud schema builders (contract §2). The store injects server timestamps where
# the contract calls for them (live.ts, meta.updated).

def live_map(r: Reading) -> dict:
    """igloos/{node}.live — latest reading per room."""
    m = {"t": r.t, "rh": r.rh, "seq": r.seq, "source": "thread"}
    if r.co2 is not None:
        m["co2"] = r.co2
    if r.batt is not None:
        m["batt"] = r.batt
    return m


def sample_doc(r: Reading) -> tuple[str, dict]:
    """igloos/{node}/samples/{epochSec} — doc id = unix seconds → idempotent (REL-03)."""
    d = {"t": r.t, "rh": r.rh, "ts": r.ts}
    if r.co2 is not None:
        d["co2"] = r.co2
    return str(r.ts), d


def room_summary(r: Reading) -> dict:
    """meta/latest.rooms.{node} — 1-read startup summary."""
    s = {"t": r.t, "rh": r.rh, "ts": r.ts}
    if r.co2 is not None:
        s["co2"] = r.co2
    return s
