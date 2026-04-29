import tkinter as tk
from tkinter import messagebox, simpledialog
from src.Park import Park
from src.Park.Ticket import Ticket
from src.Park.Exception import QueueEmptyError

class ParkGUIController:
    def __init__(self, root: tk.Tk, model: Park):
        self.model = model
        self.root = root
        self.root.title("Управление парком аттракционов")
        self.root.geometry("700x500")

        self.setup_view()
        self.update_views()

    def setup_view(self):
        # Основная сетка
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Левая колонка: Посетители
        v_frame = tk.LabelFrame(main_frame, text=" Посетители ", padx=5, pady=5)
        v_frame.grid(row=0, column=0, sticky="nsew", padx=5)

        self.list_vis = tk.Listbox(v_frame, exportselection=False, height=15)
        self.list_vis.pack(fill=tk.BOTH, expand=True)
        
        tk.Button(v_frame, text="➕ Добавить", command=self.add_visitor).pack(fill=tk.X, pady=2)
        tk.Button(v_frame, text="❌ Удалить", command=self.del_visitor).pack(fill=tk.X, pady=2)

        # Правая колонка: Аттракционы
        a_frame = tk.LabelFrame(main_frame, text=" Аттракционы ", padx=5, pady=5)
        a_frame.grid(row=0, column=1, sticky="nsew", padx=5)

        self.list_attr = tk.Listbox(a_frame, exportselection=False, height=15)
        self.list_attr.pack(fill=tk.BOTH, expand=True)

        tk.Button(a_frame, text="➕ Добавить", command=self.add_attraction).pack(fill=tk.X, pady=2)
        tk.Button(a_frame, text="❌ Удалить", command=self.del_attraction).pack(fill=tk.X, pady=2)
        tk.Button(a_frame, text="🛡️ Переключить безопасность", command=self.toggle_safety).pack(fill=tk.X, pady=2)

        # Нижняя панель: Действия
        ctrl_frame = tk.LabelFrame(self.root, text=" Управление очередью ", padx=10, pady=10)
        ctrl_frame.pack(fill=tk.X, padx=15, pady=10)

        # Кнопки действий
        tk.Button(ctrl_frame, text="🎟️ Купить билет и встать в очередь", 
                  bg="#d4edda", command=self.assign_to_attraction).grid(row=0, column=0, padx=5, sticky="ew")
        
        tk.Button(ctrl_frame, text="👤 Кто сейчас катается?", 
                  bg="#fff3cd", command=self.who_is_on).grid(row=0, column=1, padx=5, sticky="ew")

        tk.Button(ctrl_frame, text="✅ Завершить поездку (Выход)", 
                  bg="#f8d7da", command=self.finish_ride).grid(row=0, column=2, padx=5, sticky="ew")

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        ctrl_frame.columnconfigure((0,1,2), weight=1)

    def update_views(self):
        """Обновление списков без потери фокуса (по возможности)"""
        v_idx = self.list_vis.curselection()
        a_idx = self.list_attr.curselection()

        self.list_vis.delete(0, tk.END)
        for v in self.model.visitors_list:
            self.list_vis.insert(tk.END, f"ID:{v.id} | {v.full_name} (${v.wallet})")

        self.list_attr.delete(0, tk.END)
        for a in self.model.attractions_list:
            status = "OK" if a.is_safe else "ОПАСНО"
            self.list_attr.insert(tk.END, f"ID:{a.id} | {a.name} ({status})")

        if v_idx: self.list_vis.selection_set(v_idx)
        if a_idx: self.list_attr.selection_set(a_idx)

    # --- МЕТОДЫ ОБРАБОТКИ СОБЫТИЙ ---

    def add_visitor(self):
        try:
            name = simpledialog.askstring("Новый посетитель", "Имя:")
            if not name: return
            fname = simpledialog.askstring("Новый посетитель", "Фамилия:")
            lname = simpledialog.askstring("Новый посетитель", "Отчество:")
            wallet = int(simpledialog.askstring("Новый посетитель", "Баланс кошелька:"))
            self.model.create_visitor(name, fname, lname, wallet)
            self.update_views()
        except (ValueError, TypeError):
            messagebox.showerror("Ошибка", "Баланс должен быть целым числом!")

    def del_visitor(self):
        sel = self.list_vis.curselection()
        if not sel: return
        v = self.model.visitors_list[sel[0]]
        self.model.del_visitor(v.id)
        self.update_views()

    def add_attraction(self):
        name = simpledialog.askstring("Новый аттракцион", "Название:")
        if not name: return
        atype = simpledialog.askstring("Тип", "Тип (rollcoaster / carousel / ferris):")
        if atype not in ["rollcoaster", "carousel", "ferris"]:
            messagebox.showwarning("Внимание", "Неизвестный тип. Цены могут работать некорректно.")
        self.model.create_attraction(name, atype)
        self.update_views()

    def del_attraction(self):
        sel = self.list_attr.curselection()
        if not sel: return
        a = self.model.attractions_list[sel[0]]
        self.model.del_attraction(a.id)
        self.update_views()

    def toggle_safety(self):
        sel = self.list_attr.curselection()
        if not sel: return
        a = self.model.attractions_list[sel[0]]
        self.model.recheck_attraction_safety(a.id, not a.is_safe)
        self.update_views()

    def assign_to_attraction(self):
        sel_v = self.list_vis.curselection()
        sel_a = self.list_attr.curselection()
        
        if not sel_v or not sel_a:
            messagebox.showwarning("Выбор", "Выберите и посетителя, и аттракцион!")
            return
        
        v = self.model.visitors_list[sel_v[0]]
        a = self.model.attractions_list[sel_a[0]]
        
        # Проверки в контроллере для вывода нормальных ошибок
        if not a.is_safe:
            messagebox.showerror("Безопасность", f"Аттракцион '{a.name}' закрыт по тех. причинам!")
            return

        ticket = Ticket(a.type)
        if v.wallet < ticket.price:
            messagebox.showerror("Деньги", f"У {v.full_name} недостаточно средств!\nНужно: ${ticket.price}, есть: ${v.wallet}")
            return

        self.model.add_visitor_to_attraction(v.id, a.id)
        messagebox.showinfo("Успех", f"{v.full_name} успешно купил билет на '{a.name}'")
        self.update_views()

    def who_is_on(self):
        sel = self.list_attr.curselection()
        if not sel: 
            messagebox.showwarning("Выбор", "Сначала выберите аттракцион!")
            return
        
        a = self.model.attractions_list[sel[0]]
        vid = a.who_is_on
        
        if vid == -1:
            messagebox.showinfo("Статус", f"На аттракционе '{a.name}' сейчас пусто.")
        else:
            visitor = next((v for v in self.model.visitors_list if v.id == vid), None)
            name = visitor.full_name if visitor else f"ID:{vid}"
            messagebox.showinfo("В процессе", f"Сейчас катается: {name}")

    def finish_ride(self):
        sel = self.list_attr.curselection()
        if not sel: 
            messagebox.showwarning("Выбор", "Выберите аттракцион, который освободился!")
            return
        
        a = self.model.attractions_list[sel[0]]
        vid_before = a.who_is_on
        
        if vid_before == -1:
            messagebox.showwarning("Очередь", "На этом аттракционе и так никого нет.")
            return

        visitor = next((v for v in self.model.visitors_list if v.id == vid_before), None)
        name = visitor.full_name if visitor else "Посетитель"

        self.model.remove_visitor_from_attraction(a.id)
        messagebox.showinfo("Поездка окончена", f"{name} покинул аттракцион '{a.name}'.\nМесто освободилось!")
        self.update_views()