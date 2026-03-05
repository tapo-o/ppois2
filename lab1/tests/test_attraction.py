import pytest
from src.Attraction import Attraction
from src.SafetyRequirements import SafetyRequirements
from src.Visitor import Visitor
from src.Exception import QueueEmptyError


def test_attraction_safety():
    safety = SafetyRequirements()
    attr = Attraction(1, "Test", "ferris", safety)

    assert attr.is_safe is False

    attr.recheck_safety(True)
    assert attr.is_safe is True

    attr.recheck_safety(False)
    assert attr.is_safe is False


def test_who_is_on():
    safety = SafetyRequirements()
    safety.recheck(True)
    attr = Attraction(1, "Test", "carousel", safety)

    assert attr.who_is_on == -1

    v = Visitor(10, "Test", "T", "T", 50)
    attr.add_visitor(v)
    assert attr.who_is_on == 10

    attr.remove_visitor()
    assert attr.who_is_on == -1


def test_remove_from_empty():
    safety = SafetyRequirements()
    attr = Attraction(1, "Test", "ferris", safety)
    with pytest.raises(QueueEmptyError):
        attr.remove_visitor()