import sys
from src.Park.Park import Park

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

def run_cli(park: Park):
    is_work = True
    print_menu()
    while is_work:
        try:
            act = int(input("\nвыберите действие: "))
        except ValueError:
            print("Пожалуйста, введите число!")
            continue

        match act:
            case 1:
                try:
                    name = input("введите имя: ")
                    fname = input("введите фамилию: ")
                    lname = input("введите отчество: ")
                    wallet = int(input("введите сумму кошелька: "))
                    park.create_visitor(name, fname, lname, wallet)
                    print("Visitor created.")
                except ValueError:
                    print("Ошибка ввода! Введите корректные данные.")
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
                name = input("введите имя: ")
                atype = input("введите тип: ")
                park.create_attraction(name, atype)
                print("Attraction created.")
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
                    choice = int(input("input status (1. True / 2. False): "))
                    if choice == 1:
                        park.recheck_attraction_safety(iba, True)
                    elif choice == 2:
                        park.recheck_attraction_safety(iba, False)
                    else:
                        print("invalid message!")
                except ValueError:
                    print("Неверный формат ID или ввода!")
            case 12:
                print_menu()
            case 13:
                is_work = False
            case _:
                print("No command?")
                print_menu()

def run_gui(park: Park):
    import tkinter as tk
    from src.gui import ParkGUIController
    
    root = tk.Tk()
    app = ParkGUIController(root, park)
    root.mainloop()

if __name__ == "__main__":
    park_model = Park()
    
    print("Выберите режим запуска:")
    print("1. Консольный интерфейс (CLI)")
    print("2. Графический интерфейс (GUI - Tkinter)")
    
    mode = input("Ваш выбор (1 или 2): ").strip()
    
    if mode == "2":
        run_gui(park_model)
    else:
        run_cli(park_model)