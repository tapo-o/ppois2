"""Attraction class with queue and safety."""

from __future__ import annotations
from src.Queue import Queue
from src.SafetyRequirements import SafetyRequirements


class Attraction:
    def __init__(
        self, id_: int, name: str, type_: str, safety: SafetyRequirements
    ) -> None:
        self._id = id_
        self._name = name
        self._type = type_
        self._queue = Queue()
        self._safety = safety

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> str:
        return self._type

    @property
    def is_safe(self) -> bool:
        return self._safety.is_pass

    @property
    def who_is_on(self) -> int:
        """Returns visitor ID or -1 if nobody."""
        first = self._queue.get_first()
        return first.id if first else -1

    def add_visitor(self, visitor: "Visitor") -> None:
        self._queue.add_new_visitor(visitor)

    def remove_visitor(self) -> None:
        self._queue.remove_visitor()  # raises QueueEmptyError if empty

    def recheck_safety(self, status: bool) -> None:
        self._safety.recheck(status)