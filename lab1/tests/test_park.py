import pytest
from src.Park import Park
from src.Visitor import Visitor
from src.Attraction import Attraction
from src.SafetyRequirements import SafetyRequirements
from src.Ticket import Ticket
from src.Exception import (
    VisitorNotFoundError,
    AttractionNotFoundError,
    QueueEmptyError,
)


def test_create_visitor_multiple(park, monkeypatch):
    inputs = [
        "Анна", "Сергеевна", "Сидорова", "200",
        "Борис", "Алексеевич", "Иванов", "50",
    ]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))

    park.create_visitor()
    park.create_visitor()

    assert len(park._visitors) == 2
    assert 0 in park._visitors
    assert 1 in park._visitors
    assert park._visitors[0].full_name == "Анна Сергеевна Сидорова"
    assert park._visitors[1].full_name == "Борис Алексеевич Иванов"


def test_no_visitors_property(park):
    assert park.no_visitors is True

    vid = park._id_count_v
    park._id_count_v += 1
    park._visitors[vid] = Visitor(vid, "Test", "T", "T", 10)

    assert park.no_visitors is False


def test_no_attractions_property(park):
    assert park.no_attractions is True

    aid = park._id_count_a
    park._id_count_a += 1
    safety = SafetyRequirements()
    park._attractions[aid] = Attraction(aid, "Test", "carousel", safety)

    assert park.no_attractions is False


def test_del_visitor_existing(park, visitor):
    vid, _ = visitor
    assert vid in park._visitors

    park.del_visitor(vid)
    assert vid not in park._visitors


def test_del_visitor_nonexistent(park, capsys):
    park.del_visitor(777)
    captured = capsys.readouterr()
    assert "Visitor not found" in captured.out


def test_del_attraction_existing(park, safe_attraction):
    aid, _ = safe_attraction
    assert aid in park._attractions

    park.del_attraction(aid)
    assert aid not in park._attractions


def test_del_attraction_nonexistent(park, capsys):
    park.del_attraction(888)
    captured = capsys.readouterr()
    assert "Attraction not found" in captured.out


def test_add_visitor_to_attraction_success(park, visitor, safe_attraction, monkeypatch):
    vid, v = visitor
    aid, attr = safe_attraction

    # заставляем transaction всегда возвращать True и списывать деньги
    def fake_transaction(self, ticket):
        self._Visitor__wallet -= ticket.price
        return True

    monkeypatch.setattr(Visitor, "transaction", fake_transaction)

    initial_queue_size = len(attr._queue._queue)
    park.add_visitor_to_attraction(vid, aid)

    assert len(attr._queue._queue) == initial_queue_size + 1
    assert attr.who_is_on == vid


def test_add_visitor_to_attraction_unsafe(park, visitor, unsafe_attraction, capsys):
    vid, _ = visitor
    aid, attr = unsafe_attraction

    park.add_visitor_to_attraction(vid, aid)

    captured = capsys.readouterr()
    assert "not safe" in captured.out.lower()
    assert len(attr._queue._queue) == 0


def test_add_visitor_to_attraction_visitor_not_found(park, safe_attraction, capsys):
    aid, _ = safe_attraction
    park.add_visitor_to_attraction(999999, aid)

    captured = capsys.readouterr()
    assert "Visitor not found" in captured.out


def test_add_visitor_to_attraction_attraction_not_found(park, visitor, capsys):
    vid, _ = visitor
    park.add_visitor_to_attraction(vid, 999999)

    captured = capsys.readouterr()
    assert "Attraction not found" in captured.out


def test_remove_visitor_from_attraction_success(park, visitor, safe_attraction):
    vid, v = visitor
    aid, attr = safe_attraction

    attr.add_visitor(v)
    assert attr.who_is_on == vid

    park.remove_visitor_from_attraction(aid)
    assert attr.who_is_on == -1


def test_remove_visitor_from_attraction_empty(park, safe_attraction, capsys):
    aid, _ = safe_attraction
    park.remove_visitor_from_attraction(aid)

    captured = capsys.readouterr()
    assert "No one" in captured.out or "empty" in captured.out.lower()


def test_remove_visitor_from_attraction_not_found(park, capsys):
    park.remove_visitor_from_attraction(777)
    captured = capsys.readouterr()
    assert "Attraction not found" in captured.out


def test_check_attraction_no_one(park, safe_attraction, capsys):
    aid, _ = safe_attraction
    park.check_attraction(aid)

    captured = capsys.readouterr()
    assert "No one" in captured.out or "-1" in captured.out


def test_check_attraction_not_found(park, capsys):
    park.check_attraction(555)
    captured = capsys.readouterr()
    assert "Attraction not found" in captured.out


def test_recheck_attraction_safety(park, safe_attraction):
    aid, attr = safe_attraction
    assert attr.is_safe is True

    park.recheck_attraction_safety(aid, False)
    assert attr.is_safe is False

    park.recheck_attraction_safety(aid, True)
    assert attr.is_safe is True


def test_recheck_attraction_safety_not_found(park, capsys):
    park.recheck_attraction_safety(999, True)
    captured = capsys.readouterr()
    assert "Attraction not found" in captured.out


def test_check_attraction_safety(park, safe_attraction, capsys):
    aid, attr = safe_attraction

    park.check_attraction_safety(aid)
    captured = capsys.readouterr()
    assert "safe" in captured.out.lower()

    attr.recheck_safety(False)
    park.check_attraction_safety(aid)
    captured = capsys.readouterr()
    assert "not safe" in captured.out.lower()


def test_list_visitors_empty(park, capsys):
    park.list_visitors()
    captured = capsys.readouterr()
    assert "no visitors" in captured.out.lower()


def test_list_attractions_empty(park, capsys):
    park.list_attractions()
    captured = capsys.readouterr()
    assert "no attractions" in captured.out.lower()