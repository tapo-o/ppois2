import pytest
from src.Queue import Queue
from src.Visitor import Visitor
from src.Exception import QueueEmptyError


def test_queue_fifo():
    q = Queue()
    v1 = Visitor(1, "A", "A", "A", 10)
    v2 = Visitor(2, "B", "B", "B", 20)
    v3 = Visitor(3, "C", "C", "C", 30)

    q.add_new_visitor(v1)
    q.add_new_visitor(v2)
    q.add_new_visitor(v3)

    assert q.get_first().id == 1
    q.remove_visitor()
    assert q.get_first().id == 2
    q.remove_visitor()
    assert q.get_first().id == 3
    q.remove_visitor()
    assert q.get_first() is None


def test_remove_from_empty_queue():
    q = Queue()
    with pytest.raises(QueueEmptyError):
        q.remove_visitor()


def test_is_empty():
    q = Queue()
    assert q.is_empty is True

    q.add_new_visitor(Visitor(1, "x", "x", "x", 0))
    assert q.is_empty is False