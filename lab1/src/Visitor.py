from src.Ticket import Ticket


class Visitor:
    def __init__(self, id_: int, name: str, firstname: str, lastname: str, wallet: int) -> None:
        self.__id = id_
        self.__name = name
        self.__firstname = firstname
        self.__lastname = lastname
        self.__wallet = wallet

    @property
    def id(self) -> int:
        return self.__id

    @property
    def full_name(self) -> str:
        return f"{self.__name} {self.__firstname} {self.__lastname}"

    @property
    def wallet(self) -> int:
        return self.__wallet

    def transaction(self, ticket: Ticket) -> bool:
        if ticket.price > self.__wallet:
            print("no money")
            return False
        if ticket.price <= 0:
            print("ticket is not valid")
            return False

        self.__wallet -= ticket.price
        print("transaction successful")
        return True