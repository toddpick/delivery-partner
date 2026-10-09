"""Delivery slots and evening-zone availability (FEAT-047)."""

from __future__ import annotations

from datetime import time

from .models import Slot

# Slot boundaries in depot local time.
SLOT_HOURS: dict[Slot, tuple[time, time]] = {
    Slot.AM: (time(8, 0), time(12, 0)),
    Slot.PM: (time(12, 0), time(17, 0)),
    Slot.EVE: (time(17, 0), time(21, 0)),
}

# First three characters of the destination postal code for staffed evening routes.
EVENING_ZONE_PREFIXES: frozenset[str] = frozenset({"441", "442", "443", "446"})


def evening_available(postal_code: str) -> bool:
    """True if EVE can be booked for this destination postal code."""
    return postal_code.strip()[:3] in EVENING_ZONE_PREFIXES


def slot_label(slot: Slot) -> str:
    start, end = SLOT_HOURS[slot]
    return f"{start:%H:%M}-{end:%H:%M}"
