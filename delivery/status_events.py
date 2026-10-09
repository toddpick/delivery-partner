"""Builds the webhook payload sent when a parcel changes status."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from .models import ProofOfDelivery, ProofType, Status

EVENT_TYPE = "parcel.status_changed"


def depot_now() -> datetime:
    """Current time as recorded at the depot, to the second."""
    return datetime.now().replace(microsecond=0)


def _timestamp(moment: datetime | None) -> str:
    return (moment or depot_now()).isoformat()


def build_status_event(
    parcel_id: str,
    status: Status,
    client_reference: str | None = None,
    proof: ProofOfDelivery | None = None,
    occurred_at: datetime | None = None,
    event_id: str | None = None,
) -> dict[str, Any]:
    """Return the JSON-serialisable body for a status-change webhook."""
    event: dict[str, Any] = {
        "event_id": event_id or f"evt_{uuid.uuid4().hex[:10]}",
        "event_type": EVENT_TYPE,
        "parcel_id": parcel_id,
        "client_reference": client_reference,
        "status": status.value,
        "occurred_at": _timestamp(occurred_at),
    }
    if status is Status.DELIVERED and proof is not None:
        event["proof_of_delivery"] = _proof_payload(proof)
    return event


def _proof_payload(proof: ProofOfDelivery) -> dict[str, Any]:
    payload: dict[str, Any] = {"type": proof.type.value, "captured_at": proof.captured_at}
    if proof.type is ProofType.PHOTO:
        payload["photo_url"] = proof.photo_url
    else:
        payload["signed_by"] = proof.signed_by
    return payload


def capture_proof(
    proof_type: ProofType,
    photo_url: str | None = None,
    signed_by: str | None = None,
    captured_at: datetime | None = None,
) -> ProofOfDelivery:
    """Create proof-of-delivery details at the moment of handover."""
    return ProofOfDelivery(
        type=proof_type,
        captured_at=_timestamp(captured_at),
        photo_url=photo_url,
        signed_by=signed_by,
    )
