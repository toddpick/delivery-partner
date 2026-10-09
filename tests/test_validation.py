import copy
import json
from datetime import date
from pathlib import Path

from delivery.validation import validate_create_parcel

TODAY = date(2026, 10, 9)
SAMPLE = json.loads(
    (Path(__file__).parent.parent / "samples" / "create-parcel.request.json").read_text()
)


def codes(request):
    return {(e.field, e.code) for e in validate_create_parcel(request, today=TODAY)}


def variant(**changes):
    request = copy.deepcopy(SAMPLE)
    request.update(changes)
    return request


def test_sample_request_is_valid():
    assert validate_create_parcel(SAMPLE, today=TODAY) == []


def test_client_reference_limit():
    assert ("client_reference", "too_long") in codes(variant(client_reference="A" * 13))
    assert codes(variant(client_reference="A" * 12)) == set()


def test_client_reference_is_optional():
    request = variant()
    del request["client_reference"]
    assert codes(request) == set()


def test_phone_is_required():
    request = variant()
    del request["recipient"]["phone"]
    assert ("recipient.phone", "required") in codes(request)


def test_weight_limits():
    assert ("weight_kg", "too_heavy") in codes(variant(weight_kg=30.01))
    assert codes(variant(weight_kg=30.00)) == set()
    assert ("weight_kg", "invalid") in codes(variant(weight_kg=1.234))


def test_dangerous_goods_rejected():
    assert ("dangerous_goods", "not_accepted") in codes(variant(dangerous_goods=True))


def test_past_delivery_date_rejected():
    request = variant(delivery_window={"date": "2026-10-08", "slot": "PM"})
    assert ("delivery_window.date", "delivery_date_in_past") in codes(request)


def test_evening_slot_outside_zone_rejected():
    request = variant()
    request["address"]["postal_code"] = "90210"
    assert ("delivery_window.slot", "slot_unavailable_for_zone") in codes(request)


def test_daytime_slot_allowed_in_any_zone():
    request = variant(delivery_window={"date": "2026-10-20", "slot": "AM"})
    request["address"]["postal_code"] = "90210"
    assert codes(request) == set()
