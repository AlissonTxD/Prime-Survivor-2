from sys import argv, exit

from PyQt5.QtWidgets import QApplication

from src.views.view_main import MainWindow
from src.controllers.controller_main import MainController


def start():
    app = QApplication(argv)
    view = MainWindow()
    controller = MainController(view)
    view.show()
    exit(app.exec_())
