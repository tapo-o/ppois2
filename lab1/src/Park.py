from src.Visitor import Visitor
from src.Attraction import Attraction
from src.Ticket import Ticket
from src.Exception import QueueEmptyError
from src.SafetyRequirements import SafetyRequirements


class Park:
    def __init__(self) -> None:
        self._visitors: dict[int, Visitor] = {}
        self._attractions: dict[int, Attraction] = {}
        self._id_count_v = 0
        self._id_count_a = 0

    @property
    def no_visitors(self) -> bool:
        return not self._visitors

    @property
    def no_attractions(self) -> bool:
        return not self._attractions

    def create_visitor(self) -> None:
        try:
            name = input("введите имя: ")
            firstname = input("введите фамилию: ")
            lastname = input("введите отчество: ")
            wallet = int(input("введите сумму кошелька: "))
        except ValueError:
            print("Ошибка ввода! Введите корректные данные.")
            return

        vid = self._id_count_v
        self._visitors[vid] = Visitor(vid, name, firstname, lastname, wallet)
        self._id_count_v += 1
        print(f"Visitor {vid} created.")

    def list_visitors(self) -> None:
        if self.no_visitors:
            print("no visitors")
            return
        for vid, visitor in self._visitors.items():
            print(vid, visitor.full_name, visitor.wallet)

    def del_visitor(self, vid: int) -> None:
        if vid in self._visitors:
            del self._visitors[vid]
            print(f"Visitor {vid} deleted.")
        else:
            print("Visitor not found")

    def create_attraction(self) -> None:
        name = input("введите имя: ")
        atype = input("введите тип: ")
        aid = self._id_count_a
        self._attractions[aid] = Attraction(aid, name, atype, SafetyRequirements())
        self._id_count_a += 1
        print(f"Attraction {aid} created.")

    def list_attractions(self) -> None:
        if self.no_attractions:
            print("no attractions")
            return
        for aid, attr in self._attractions.items():
            print(aid, attr.name)

    def del_attraction(self, aid: int) -> None:
        if aid in self._attractions:
            del self._attractions[aid]
            print(f"Attraction {aid} deleted.")
        else:
            print("Attraction not found")

    def add_visitor_to_attraction(self, vid: int, aid: int) -> None:
        if vid not in self._visitors:
            print("Visitor not found")
            return
        if aid not in self._attractions:
            print("Attraction not found")
            return

        if self.no_visitors or self.no_attractions:
            print("no visitors or attractions")
            return

        attraction = self._attractions[aid]
        if not attraction.is_safe:
            print("attraction is not safe")
            return

        ticket = Ticket(attraction.type)
        visitor = self._visitors[vid]
        if visitor.transaction(ticket):
            attraction.add_visitor(visitor)
            print("Visitor added to attraction queue")
        else:
            print("something went wrong")

    def remove_visitor_from_attraction(self, aid: int) -> None:
        if aid not in self._attractions:
            print("Attraction not found")
            return
        try:
            self._attractions[aid].remove_visitor()
            print("Visitor removed from attraction")
        except QueueEmptyError:
            print("No one on the attraction")

    def check_attraction(self, aid: int) -> None:
        if aid not in self._attractions:
            print("Attraction not found")
            return
        ib = self._attractions[aid].who_is_on
        if ib == -1:
            print("No one on attraction")
        else:
            self.check_visitor(ib)

    def check_visitor(self, vid: int) -> None:
        if vid not in self._visitors:
            print("Visitor not found")
            return
        v = self._visitors[vid]
        print(v.id, v.full_name, v.wallet)

    def check_attraction_safety(self, aid: int) -> None:
        if aid not in self._attractions:
            print("Attraction not found")
            return
        print(
            "attraction is safe"
            if self._attractions[aid].is_safe
            else "attraction is not safe"
        )

    def recheck_attraction_safety(self, aid: int, status: bool) -> None:
        if aid not in self._attractions:
            print("Attraction not found")
            return
        self._attractions[aid].recheck_safety(status)