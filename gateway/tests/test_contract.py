import json

import cbor2
import pytest

from bridge import contract
from bridge.contract import ContractError

NOW = 1_752_300_000


def valid_payload(**overrides):
    p = {"node": "iglu_1", "fw": "0.1.0", "seq": 7, "up_ms": 1000, "t": 21.4, "rh": 88.2}
    p.update(overrides)
    return p


def test_parse_cbor():
    r = contract.parse(cbor2.dumps(valid_payload()), now=lambda: NOW)
    assert (r.node, r.seq, r.t, r.rh, r.ts) == ("iglu_1", 7, 21.4, 88.2, NOW)
    assert r.co2 is None and r.batt is None


def test_parse_json_fallback():
    r = contract.parse(json.dumps(valid_payload(co2=920, batt=2960)).encode(), now=lambda: NOW)
    assert r.co2 == 920 and r.batt == 2960


def test_rejects_garbage():
    with pytest.raises(ContractError):
        contract.parse(b"\xff\x00 not a payload")


def test_rejects_missing_field():
    p = valid_payload()
    del p["rh"]
    with pytest.raises(ContractError, match="missing"):
        contract.parse(cbor2.dumps(p))


def test_rejects_unknown_field():
    with pytest.raises(ContractError, match="unknown"):
        contract.parse(cbor2.dumps(valid_payload(extra=1)))


@pytest.mark.parametrize("field,value", [
    ("t", -5), ("t", 51), ("rh", 101), ("co2", 200), ("co2", 9000), ("batt", 4000),
])
def test_rejects_out_of_range(field, value):
    with pytest.raises(ContractError, match=field):
        contract.parse(cbor2.dumps(valid_payload(**{field: value})))


def test_rejects_negative_seq():
    with pytest.raises(ContractError, match="seq"):
        contract.parse(cbor2.dumps(valid_payload(seq=-1)))


def test_cloud_schema_builders():
    r = contract.parse(cbor2.dumps(valid_payload(co2=920)), now=lambda: NOW)
    assert contract.live_map(r) == {"t": 21.4, "rh": 88.2, "co2": 920, "seq": 7,
                                    "source": "thread"}
    doc_id, doc = contract.sample_doc(r)
    assert doc_id == str(NOW)  # unix-seconds doc id → idempotent (REL-03)
    assert doc == {"t": 21.4, "rh": 88.2, "co2": 920, "ts": NOW}
    assert contract.room_summary(r) == {"t": 21.4, "rh": 88.2, "co2": 920, "ts": NOW}


def test_optional_fields_omitted_when_absent():
    r = contract.parse(cbor2.dumps(valid_payload()), now=lambda: NOW)
    assert "co2" not in contract.live_map(r)
    assert "batt" not in contract.live_map(r)
    assert "co2" not in contract.sample_doc(r)[1]
