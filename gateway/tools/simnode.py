"""Simulated sensor node (Phase 0): POSTs contract-shaped CBOR telemetry over CoAP.

Stands in for the nRF52840 node until firmware lands; lets the bridge, Firestore
schema, and app live-tile be proven end-to-end with no hardware (POC-06/08/09).

    python tools/simnode.py --node iglu_1 --interval 5 [--host ::1]
"""

import argparse
import asyncio
import logging
import random

import aiocoap
import cbor2

log = logging.getLogger("simnode")


async def run(host: str, node: str, interval: float) -> None:
    ctx = await aiocoap.Context.create_client_context()
    seq = 0
    up_ms = 0
    # plausible mushroom-room conditions, drifting slowly
    t, rh = 21.0, 88.0
    while True:
        t = min(24.0, max(18.0, t + random.uniform(-0.2, 0.2)))
        rh = min(95.0, max(82.0, rh + random.uniform(-0.5, 0.5)))
        payload = cbor2.dumps({
            "node": node, "fw": "sim-0.1.0", "seq": seq, "up_ms": up_ms,
            "t": round(t, 1), "rh": round(rh, 1),
        })
        msg = aiocoap.Message(code=aiocoap.POST, uri=f"coap://{host}/telemetry",
                              payload=payload)
        try:
            resp = await ctx.request(msg).response
            log.info("seq=%d t=%.1f rh=%.1f -> %s", seq, t, rh, resp.code)
        except Exception as e:
            log.warning("seq=%d send failed: %s", seq, e)
        seq += 1
        up_ms += int(interval * 1000)
        await asyncio.sleep(interval)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--host", default="::1")
    ap.add_argument("--node", default="iglu_1")
    ap.add_argument("--interval", type=float, default=30.0, help="seconds (POC-02)")
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    asyncio.run(run(args.host, args.node, args.interval))
