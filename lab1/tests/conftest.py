import pytest
from src.Park import Park
from src.Visitor import Visitor
from src.Attraction import Attraction
from src.SafetyRequirements import SafetyRequirements


@pytest.fixture
def park():
    return Park()


@pytest.fixture
def visitor(park):
    vid = park._id_count_v
    park._id_count_v += 1
    v = Visitor(vid, "Тест", "Тестович", "Тестов", 100)
    park._visitors[vid] = v
    return vid, v


@pytest.fixture
def safe_attraction(park):
    aid = park._id_count_a
    park._id_count_a += 1
    safety = SafetyRequirements()
    safety.recheck(True)
    attr = Attraction(aid, "Safe Ferris", "ferris", safety)
    park._attractions[aid] = attr
    return aid, attr


@pytest.fixture
def unsafe_attraction(park):
    aid = park._id_count_a
    park._id_count_a += 1
    safety = SafetyRequirements()  # False по умолчанию
    attr = Attraction(aid, "Broken Coaster", "rollcoaster", safety)
    park._attractions[aid] = attr
    return aid, attr