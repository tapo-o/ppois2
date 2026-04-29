from __future__ import annotations
from .Exception import QueueEmptyError


class Queue:
    def __init__(self) -> None:
        self._queue: list["Visitor"] = []

    def add_new_visitor(self, visitor: "Visitor") -> None:
        self._queue.append(visitor)

    def remove_visitor(self) -> None:
        if not self._queue:
            raise QueueEmptyError("No visitors in the queue")
        self._queue.pop(0)

    def get_first(self) -> "Visitor | None":
        return self._queue[0] if self._queue else None

    @property
    def is_empty(self) -> bool:
        return len(self._queue) == 0