import json
from pathlib import Path

from delivery.models import ProofType, Status
from delivery.status_events import build_status_event, capture_proof

SAMPLES = Path(__file__).parent.parent / "samples"
BASE_KEYS = {"event_id", "event_type", "parcel_id", "client_reference", "status", "occurred_at"}


def test_event_has_expected_keys():
    event = build_status_event("DP-7Q4K2M9X", Status.OUT_FOR_DELIVERY, client_reference="A-10482")
    assert set(event) == BASE_KEYS
    assert event["event_type"] == "parcel.status_changed"
    assert event["status"] == "OUT_FOR_DELIVERY"
    assert isinstance(event["occurred_at"], str)


def test_event_is_json_serialisable():
    json.dumps(build_status_event("DP-7Q4K2M9X", Status.AT_DEPOT))


def test_client_reference_is_echoed_or_null():
    assert build_status_event("DP-7Q4K2M9X", Status.CREATED, "A-1")["client_reference"] == "A-1"
    assert build_status_event("DP-7Q4K2M9X", Status.CREATED)["client_reference"] is None


def test_delivered_event_carries_proof():
    proof = capture_proof(ProofType.PHOTO, photo_url="https://pod.delivery-partner.example/p/1.jpg")
    event = build_status_event("DP-7Q4K2M9X", Status.DELIVERED, proof=proof)
    assert set(event) == BASE_KEYS | {"proof_of_delivery"}
    assert event["proof_of_delivery"]["type"] == "PHOTO"
    assert "photo_url" in event["proof_of_delivery"]


def test_proof_is_only_sent_on_delivered():
    proof = capture_proof(ProofType.SIGNATURE, signed_by="Sam Patel")
    event = build_status_event("DP-7Q4K2M9X", Status.FAILED_ATTEMPT, proof=proof)
    assert "proof_of_delivery" not in event


def test_samples_match_event_shape():
    for name in ("webhook.delivered.json", "webhook.held-at-depot.json"):
        sample = json.loads((SAMPLES / name).read_text())
        assert BASE_KEYS <= set(sample)
        assert sample["status"] in {s.value for s in Status}
