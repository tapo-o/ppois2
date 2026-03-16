from tkinter import messagebox, filedialog
from model.athlete import Athlete

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.current_page = 1
        self.page_size = 10
        self.view.btn_prev.config(command=self.prev)
        self.view.btn_next.config(command=self.next)
        self._init_menu()
        self.refresh()

    def _init_menu(self):
        self.view.add_btn("Добавить", self.add)
        self.view.add_btn("Поиск", self.search)
        self.view.add_btn("Удалить", self.delete)
        self.view.add_btn("Загрузить", self.load)
        self.view.add_btn("Сохранить", self.save)

    def refresh(self):
        data = self.model.get_page(self.current_page, self.page_size)
        total = self.model.total_pages(self.page_size)
        self.view.update_table(data, self.current_page, total, self.page_size)

    def next(self):
        if self.current_page < self.model.total_pages(self.page_size):
            self.current_page += 1
            self.refresh()

    def prev(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.refresh()

    def add(self):
        from view.dialogs import AddDialog
        d = AddDialog(self.view)
        self.view.wait_window(d)
        if d.result:
            self.model.add_athlete(Athlete(*d.result))
            self.refresh()

    def search(self):
        from view.dialogs import SearchDialog
        SearchDialog(self.view, [], self.model.search)

    def delete(self):
        from view.dialogs import DeleteDialog
        d = DeleteDialog(self.view)
        self.view.wait_window(d)
        if d.result:
            num = self.model.delete(fio=d.result[0])
            messagebox.showinfo("Инфо", f"Удалено: {num}")
            self.refresh()

    def load(self):
        p = filedialog.askopenfilename()
        if p:
            self.model.load_xml(p)
            self.current_page = 1
            self.refresh()

    def save(self):
        p = filedialog.asksaveasfilename(defaultextension=".xml")
        if p: self.model.save_xml(p)