"""Validation of a create-parcel request (POST /v1/parcels)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Any

from .models import Slot
from .windows import evening_available

MAX_WEIGHT_KG = Decimal("30.00")
MAX_CLIENT_REFERENCE = 12
PHONE_PATTERN = re.compile(r"^\+[1-9]\d{7,14}$")
ADDRESS_REQUIRED = ("street1", "city", "region", "postal_code", "country_code")


@dataclass(frozen=True)
class ValidationError:
    field: str
    code: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {"field": self.field, "code": self.code, "message": self.message}


def _blank(value: Any) -> bool:
    return not isinstance(value, str) or not value.strip()


def validate_create_parcel(request: dict[str, Any], today: date | None = None) -> list[ValidationError]:
    """Return all problems found; an empty list means the request is valid."""
    today = today or date.today()
    errors: list[ValidationError] = []

    reference = request.get("client_reference")
    if reference is not None and (not isinstance(reference, str) or len(reference) > MAX_CLIENT_REFERENCE):
        errors.append(ValidationError(
            "client_reference", "too_long",
            f"client_reference must be at most {MAX_CLIENT_REFERENCE} characters"))

    recipient = request.get("recipient") or {}
    if _blank(recipient.get("name")):
        errors.append(ValidationError("recipient.name", "required", "recipient name is required"))
    phone = recipient.get("phone")
    if _blank(phone):
        errors.append(ValidationError("recipient.phone", "required", "recipient phone is required"))
    elif not PHONE_PATTERN.match(phone):
        errors.append(ValidationError("recipient.phone", "invalid_format", "phone must be E.164"))

    address = request.get("address") or {}
    for name in ADDRESS_REQUIRED:
        if _blank(address.get(name)):
            errors.append(ValidationError(f"address.{name}", "required", f"{name} is required"))

    errors.extend(_validate_weight(request.get("weight_kg")))

    dims = request.get("dimensions_cm") or {}
    for name in ("length", "width", "height"):
        value = dims.get(name)
        if not isinstance(value, int) or isinstance(value, bool) or value < 1:
            errors.append(ValidationError(
                f"dimensions_cm.{name}", "invalid", f"{name} must be a whole number of centimetres"))

    if request.get("dangerous_goods") is True:
        errors.append(ValidationError(
            "dangerous_goods", "not_accepted", "hazardous goods are not accepted"))

    errors.extend(_validate_window(request.get("delivery_window") or {}, address, today))
    return errors


def _validate_weight(raw: Any) -> list[ValidationError]:
    try:
        weight = Decimal(str(raw))
    except (InvalidOperation, ValueError):
        return [ValidationError("weight_kg", "invalid", "weight_kg must be a decimal number")]
    if weight <= 0:
        return [ValidationError("weight_kg", "invalid", "weight_kg must be greater than zero")]
    if weight != weight.quantize(Decimal("0.01")):
        return [ValidationError("weight_kg", "invalid", "weight_kg allows at most 2 decimal places")]
    if weight > MAX_WEIGHT_KG:
        return [ValidationError("weight_kg", "too_heavy", f"weight_kg must not exceed {MAX_WEIGHT_KG}")]
    return []


def _validate_window(window: dict[str, Any], address: dict[str, Any], today: date) -> list[ValidationError]:
    errors: list[ValidationError] = []
    try:
        slot = Slot(window.get("slot"))
    except ValueError:
        return [ValidationError("delivery_window.slot", "invalid", "slot must be AM, PM or EVE")]

    try:
        day = date.fromisoformat(str(window.get("date")))
    except ValueError:
        return [ValidationError("delivery_window.date", "invalid", "date must be YYYY-MM-DD")]

    if day < today:
        errors.append(ValidationError(
            "delivery_window.date", "delivery_date_in_past", "delivery date must be today or later"))
    if slot is Slot.EVE and not evening_available(str(address.get("postal_code") or "")):
        errors.append(ValidationError(
            "delivery_window.slot", "slot_unavailable_for_zone",
            "EVE is not available for this postal code"))
    return errors
