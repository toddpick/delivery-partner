"""Core types for parcels and status events."""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from enum import StrEnum


class Status(StrEnum):
    CREATED = "CREATED"
    LABELLED = "LABELLED"
    COLLECTED = "COLLECTED"
    AT_DEPOT = "AT_DEPOT"
    HELD_AT_DEPOT = "HELD_AT_DEPOT"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    DELIVERED = "DELIVERED"
    FAILED_ATTEMPT = "FAILED_ATTEMPT"
    RETURNED_TO_SENDER = "RETURNED_TO_SENDER"


class Slot(StrEnum):
    AM = "AM"
    PM = "PM"
    EVE = "EVE"


class ProofType(StrEnum):
    PHOTO = "PHOTO"
    SIGNATURE = "SIGNATURE"


@dataclass(frozen=True)
class Recipient:
    name: str
    phone: str


@dataclass(frozen=True)
class Address:
    street1: str
    city: str
    region: str
    postal_code: str
    country_code: str
    street2: str | None = None


@dataclass(frozen=True)
class Dimensions:
    length: int
    width: int
    height: int


@dataclass(frozen=True)
class DeliveryWindow:
    date: str  # YYYY-MM-DD, depot local date
    slot: Slot


@dataclass(frozen=True)
class ProofOfDelivery:
    type: ProofType
    captured_at: str
    photo_url: str | None = None
    signed_by: str | None = None


@dataclass
class Parcel:
    parcel_id: str
    recipient: Recipient
    address: Address
    weight_kg: Decimal
    dimensions_cm: Dimensions
    delivery_window: DeliveryWindow
    client_reference: str | None = None
    special_handling: bool = False
    signature_service: bool = False
    status: Status = Status.CREATED
    history: list[Status] = field(default_factory=list)
