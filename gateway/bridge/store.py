"""Cloud write-side. FirestoreStore is the real thing; MemoryStore backs tests/dry-run."""

import logging
from typing import Protocol

from . import contract
from .contract import Reading

log = logging.getLogger(__name__)


class Store(Protocol):
    def write_reading(self, r: Reading) -> None: ...


class MemoryStore:
    """In-memory mirror of the cloud schema — dry-run and tests."""

    def __init__(self):
        self.live: dict[str, dict] = {}
        self.samples: dict[str, dict[str, dict]] = {}
        self.rooms: dict[str, dict] = {}

    def write_reading(self, r: Reading) -> None:
        self.live[r.node] = contract.live_map(r) | {"ts": r.ts}
        doc_id, doc = contract.sample_doc(r)
        self.samples.setdefault(r.node, {})[doc_id] = doc
        self.rooms[r.node] = contract.room_summary(r)
        log.info("write %s seq=%s t=%.1f rh=%.1f", r.node, r.seq, r.t, r.rh)


class FirestoreStore:
    """Writes the three contract docs per reading. Holds the only cloud credential
    in the system (GW-05)."""

    def __init__(self, credentials_path: str | None = None):
        # Imported here so tests and --dry-run never need the GCP stack.
        from google.cloud import firestore

        if credentials_path:
            self._db = firestore.Client.from_service_account_json(credentials_path)
        else:
            self._db = firestore.Client()
        self._sentinel = firestore.SERVER_TIMESTAMP

    def write_reading(self, r: Reading) -> None:
        batch = self._db.batch()
        batch.set(
            self._db.collection("igloos").document(r.node),
            {"live": contract.live_map(r) | {"ts": self._sentinel}},
            merge=True,
        )
        doc_id, doc = contract.sample_doc(r)
        batch.set(
            self._db.collection("igloos").document(r.node).collection("samples").document(doc_id),
            doc,
        )
        batch.set(
            self._db.collection("meta").document("latest"),
            {"rooms": {r.node: contract.room_summary(r)}, "updated": self._sentinel},
            merge=True,
        )
        batch.commit()
        log.info("firestore write %s seq=%s", r.node, r.seq)
