import tkinter as tk
from tkinter import ttk

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sports Manager")
        self.geometry("1200x500")

        self.toolbar = ttk.Frame(self)
        self.toolbar.pack(side="top", fill="x")

        cols = ("num", "n", "s", "p", "t", "sp", "r")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        for c, h in zip(cols, ["№", "ФИО", "Состав", "Позиция", "Титулы", "Спорт", "Разряд"]):
            self.tree.heading(c, text=h)
        self.tree.column("num", width=40, anchor="center")
        self.tree.pack(expand=True, fill="both")

        self.nav_frame = ttk.Frame(self)
        self.nav_frame.pack(side="bottom", fill="x", pady=5)
        self.btn_prev = ttk.Button(self.nav_frame, text="⬅")
        self.btn_prev.pack(side="left", padx=20)
        self.page_label = ttk.Label(self.nav_frame, text="Страница: 1/1")
        self.page_label.pack(side="left", expand=True)
        self.btn_next = ttk.Button(self.nav_frame, text="➡")
        self.btn_next.pack(side="right", padx=20)

        self.menu = tk.Menu(self)
        self.config(menu=self.menu)
        self.file_m = tk.Menu(self.menu, tearoff=0)
        self.edit_m = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Файл", menu=self.file_m)
        self.menu.add_cascade(label="Правка", menu=self.edit_m)

    def add_btn(self, text, cmd):
        ttk.Button(self.toolbar, text=text, command=cmd).pack(side="left", padx=2)
        target = self.file_m if "Загрузить" in text or "Сохранить" in text else self.edit_m
        target.add_command(label=text, command=cmd)

    def update_table(self, data, page, total, page_size):
        self.tree.delete(*self.tree.get_children())
        start_idx = (page - 1) * page_size + 1
        for i, a in enumerate(data, start=start_idx):
            self.tree.insert("", "end", values=(i, a.full_name, a.squad, a.position, a.titles, a.sport, a.rank))
        self.page_label.config(text=f"Страница: {page} / {max(1, total)}")