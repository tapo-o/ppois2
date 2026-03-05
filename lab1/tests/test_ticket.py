import pytest
from src.Ticket import Ticket
from src.consts import ROLLER_COASTER, CAROUSEL, FERRIS_WHEEL


@pytest.mark.parametrize("type_, expected_price", [
    (ROLLER_COASTER, 9),
    (CAROUSEL, 5),
    (FERRIS_WHEEL, 7),
    ("something-else", -1),
    ("", -1),
    (None, -1),
])
def test_ticket_price(type_, expected_price):
    t = Ticket(type_)
    assert t.price == expected_price
    assert t.type == type_