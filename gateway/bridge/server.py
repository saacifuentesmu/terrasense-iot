"""CoAP server: POST /telemetry → validate per contract → write to the store (POC-04/06)."""

import logging

import aiocoap
import aiocoap.resource as resource

from . import contract
from .store import Store

log = logging.getLogger(__name__)


class TelemetryResource(resource.Resource):
    def __init__(self, store: Store):
        super().__init__()
        self._store = store
        self._last_seq: dict[str, int] = {}

    async def render_post(self, request):
        try:
            r = contract.parse(request.payload)
        except contract.ContractError as e:
            log.warning("rejected payload: %s", e)
            return aiocoap.Message(code=aiocoap.BAD_REQUEST, payload=str(e).encode())

        # Confirmable retries may replay a reading; ACK duplicates without rewriting.
        if self._last_seq.get(r.node) == r.seq:
            log.debug("duplicate %s seq=%s", r.node, r.seq)
            return aiocoap.Message(code=aiocoap.CHANGED, payload=b"dup")

        self._store.write_reading(r)
        self._last_seq[r.node] = r.seq
        return aiocoap.Message(code=aiocoap.CHANGED)


async def make_context(store: Store, bind: str = "::") -> aiocoap.Context:
    root = resource.Site()
    root.add_resource(["telemetry"], TelemetryResource(store))
    return await aiocoap.Context.create_server_context(root, bind=(bind, aiocoap.COAP_PORT))
