from src.Park import Park
from src.SafetyRequirements import SafetyRequirements


is_work = True


def print_menu() -> None:
    print("<==========|Menu|==========>")
    print("1. add new visitor")
    print("2. list visitors")
    print("3. del visitor")
    print("4. add attraction")
    print("5. list attractions")
    print("6. del attraction")
    print("7. add visitor to queue")
    print("8. who is on attraction")
    print("9. end attraction (next)")
    print("10. check attraction safety")
    print("11. recheck attraction safety")
    print("12. help")
    print("13. exit")


if __name__ == "__main__":
    print_menu()
    park = Park()

    while is_work:
        try:
            act = int(input("выберите действие: "))
        except ValueError:
            print("Пожалуйста, введите число!")
            continue

        match act:
            case 1:
                park.create_visitor()

            case 2:
                park.list_visitors()

            case 3:
                if park.no_visitors:
                    print("no visitors")
                else:
                    try:
                        ib = int(input("id: "))
                        park.del_visitor(ib)
                    except ValueError:
                        print("Неверный формат ID!")

            case 4:
                park.create_attraction()

            case 5:
                park.list_attractions()

            case 6:
                if park.no_attractions:
                    print("no attractions")
                else:
                    try:
                        ib = int(input("id: "))
                        park.del_attraction(ib)
                    except ValueError:
                        print("Неверный формат ID!")

            case 7:
                try:
                    ibv = int(input("visitor id: "))
                    iba = int(input("attraction id: "))
                    park.add_visitor_to_attraction(ibv, iba)
                except ValueError:
                    print("Неверный формат ID!")

            case 8:
                if park.no_attractions:
                    print("no attractions")
                else:
                    try:
                        ib = int(input("attraction id: "))
                        park.check_attraction(ib)
                    except ValueError:
                        print("Неверный формат ID!")

            case 9:
                try:
                    iba = int(input("attraction id: "))
                    park.remove_visitor_from_attraction(iba)
                except ValueError:
                    print("Неверный формат ID!")

            case 10:
                try:
                    iba = int(input("attraction id: "))
                    park.check_attraction_safety(iba)
                except ValueError:
                    print("Неверный формат ID!")

            case 11:
                try:
                    iba = int(input("attraction id: "))
                    print("input status:")
                    print("1. True")
                    print("2. False")
                    chicking = True
                    while chicking:
                        try:
                            choice = int(input())
                        except ValueError:
                            print("invalid number!")
                            continue
                        match choice:
                            case 1:
                                pas = True
                                chicking = False
                            case 2:
                                pas = False
                                chicking = False
                            case _:
                                print("invalid message!")
                                continue
                    park.recheck_attraction_safety(iba, pas)
                except ValueError:
                    print("Неверный формат ID!")

            case 12:
                print_menu()

            case 13:
                is_work = False

            case _:
                print("No command?")
                print_menu()