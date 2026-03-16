from model.data_manager import DataManager
from view.main_window import MainWindow
from controller.main_controller import Controller

if __name__ == "__main__":
    model = DataManager()
    view = MainWindow()
    controller = Controller(model, view)
    view.mainloop()