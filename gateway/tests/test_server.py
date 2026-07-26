"""CoAP round-trip: client POST → TelemetryResource → MemoryStore (loopback, no network)."""

import aiocoap
import cbor2
import pytest

from bridge.server import TelemetryResource
from bridge.store import MemoryStore


@pytest.fixture
async def coap(unused_udp_port_factory=None):
    store = MemoryStore()
    root = aiocoap.resource.Site()
    root.add_resource(["telemetry"], TelemetryResource(store))
    server = await aiocoap.Context.create_server_context(root, bind=("::1", 56831))
    client = await aiocoap.Context.create_client_context()
    yield client, store
    await client.shutdown()
    await server.shutdown()


def payload(seq=1, **overrides):
    p = {"node": "iglu_1", "fw": "0.1.0", "seq": seq, "up_ms": 1000, "t": 21.4, "rh": 88.2}
    p.update(overrides)
    return cbor2.dumps(p)


async def post(client, body):
    msg = aiocoap.Message(code=aiocoap.POST, uri="coap://[::1]:56831/telemetry", payload=body)
    return await client.request(msg).response


async def test_valid_reading_is_stored(coap):
    client, store = coap
    resp = await post(client, payload(seq=1))
    assert resp.code == aiocoap.CHANGED
    assert store.live["iglu_1"]["seq"] == 1
    assert store.rooms["iglu_1"]["t"] == 21.4
    assert len(store.samples["iglu_1"]) == 1


async def test_bad_payload_rejected_and_not_stored(coap):
    client, store = coap
    resp = await post(client, b"junk")
    assert resp.code == aiocoap.BAD_REQUEST
    assert store.live == {}


async def test_duplicate_seq_acked_but_not_rewritten(coap):
    client, store = coap
    await post(client, payload(seq=5))
    resp = await post(client, payload(seq=5, t=30.0))  # CON retry replay
    assert resp.code == aiocoap.CHANGED
    assert store.live["iglu_1"]["t"] == 21.4  # first write wins
