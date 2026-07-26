"""Run the bridge: `python -m bridge --dry-run` or with a service account for Firestore."""

import argparse
import asyncio
import logging


async def main() -> None:
    ap = argparse.ArgumentParser(description="TerraSense CoAP → Firestore bridge")
    ap.add_argument("--bind", default="::", help="address to bind the CoAP server to")
    ap.add_argument("--credentials", help="path to the service-account JSON (GW-05)")
    ap.add_argument("--dry-run", action="store_true", help="log writes in memory, no cloud")
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    if args.dry_run:
        from .store import MemoryStore

        store = MemoryStore()
    else:
        from .store import FirestoreStore

        store = FirestoreStore(credentials_path=args.credentials)

    from .server import make_context

    await make_context(store, bind=args.bind)
    logging.info("bridge listening on coap://[%s]/telemetry (%s)",
                 args.bind, "dry-run" if args.dry_run else "firestore")
    await asyncio.get_running_loop().create_future()  # serve forever


if __name__ == "__main__":
    asyncio.run(main())
