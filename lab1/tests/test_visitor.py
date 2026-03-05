import pytest
from src.Visitor import Visitor
from src.Ticket import Ticket


def test_visitor_transaction_success():
    v = Visitor(1, "Иван", "И.", "Петров", 100)
    ticket = Ticket("carousel")  # 5
    assert v.wallet == 100
    success = v.transaction(ticket)
    assert success is True
    assert v.wallet == 95


def test_visitor_transaction_not_enough():
    v = Visitor(1, "Иван", "И.", "Петров", 4)
    ticket = Ticket("carousel")  # 5
    success = v.transaction(ticket)
    assert success is False
    assert v.wallet == 4


def test_visitor_transaction_invalid_ticket():
    v = Visitor(1, "Иван", "И.", "Петров", 100)
    ticket = Ticket("unknown")  # -1
    success = v.transaction(ticket)
    assert success is False