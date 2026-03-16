import tkinter as tk
from tkinter import ttk

class AddDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Добавить")
        self.result = None
        self.grab_set()
        fields = [("ФИО", "f"), ("Состав", "s"), ("Позиция", "p"), ("Титулы", "t"), ("Спорт", "sp"), ("Разряд", "r")]
        self.inputs = {}
        for i, (l, k) in enumerate(fields):
            ttk.Label(self, text=l).grid(row=i, column=0, padx=5, pady=5)
            w = ttk.Entry(self)
            w.grid(row=i, column=1, padx=5, pady=5)
            self.inputs[k] = w
        ttk.Button(self, text="ОК", command=self.confirm).grid(row=6, column=0, columnspan=2)

    def confirm(self):
        self.result = [v.get() for v in self.inputs.values()]
        self.destroy()

class SearchDialog(tk.Toplevel):
    def __init__(self, parent, sports, callback):
        super().__init__(parent)
        self.title("Поиск")
        self.callback = callback
        frame = ttk.Frame(self, padding=10)
        frame.pack()
        ttk.Label(frame, text="ФИО:").grid(row=0, column=0)
        self.f = ttk.Entry(frame); self.f.grid(row=0, column=1)
        ttk.Button(frame, text="Найти", command=self.do).grid(row=1, column=0, columnspan=2)
        self.tree = ttk.Treeview(self, columns=(0,1,2,3,4,5,6), show="headings", height=5)
        for i, h in enumerate(["№", "ФИО", "Сост", "Поз", "Тит", "Спорт", "Разр"]):
            self.tree.heading(i, text=h); self.tree.column(i, width=70)
        self.tree.pack()

    def do(self):
        res = self.callback(fio=self.f.get())
        self.tree.delete(*self.tree.get_children())
        for i, a in enumerate(res, 1):
            self.tree.insert("", "end", values=(i, a.full_name, a.squad, a.position, a.titles, a.sport, a.rank))

class DeleteDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.result = None
        self.grab_set()
        ttk.Label(self, text="ФИО для удаления:").pack()
        self.e = ttk.Entry(self); self.e.pack()
        ttk.Button(self, text="Удалить", command=self.ok).pack()

    def ok(self):
        self.result = (self.e.get(), None)
        self.destroy()