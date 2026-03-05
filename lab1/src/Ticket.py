from src.consts import (
    ROLLER_COASTER,
    CAROUSEL,
    FERRIS_WHEEL,
    ROLLER_COASTER_PRICE,
    CAROUSEL_PRICE,
    FERRIS_WHEEL_PRICE,
)


class Ticket:
    def __init__(self, type_: str) -> None:
        self._type = type_
        match type_:
            case "rollcoaster":
                self._price = ROLLER_COASTER_PRICE
            case "carousel":
                self._price = CAROUSEL_PRICE
            case "ferris":
                self._price = FERRIS_WHEEL_PRICE
            case _:
                self._price = -1

    @property
    def price(self) -> int:
        return self._price

    @property
    def type(self) -> str:
        return self._type