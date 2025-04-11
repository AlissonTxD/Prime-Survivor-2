from sys import argv, exit

from PyQt5.QtWidgets import QApplication

from src.view.view_main import MainWindow

def start():
    app = QApplication(argv)
    view = MainWindow()
    view.show()
    exit(app.exec_())