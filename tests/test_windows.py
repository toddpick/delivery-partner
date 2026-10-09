from datetime import time

from delivery.models import Slot
from delivery.windows import SLOT_HOURS, evening_available, slot_label


def test_slot_hours():
    assert SLOT_HOURS[Slot.AM] == (time(8), time(12))
    assert SLOT_HOURS[Slot.PM] == (time(12), time(17))
    assert SLOT_HOURS[Slot.EVE] == (time(17), time(21))


def test_slot_label():
    assert slot_label(Slot.EVE) == "17:00-21:00"


def test_evening_zone_membership():
    assert evening_available("44114")
    assert evening_available(" 44301 ")
    assert not evening_available("90210")
    assert not evening_available("")
