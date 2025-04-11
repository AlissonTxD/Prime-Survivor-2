from PyQt5.QtWidgets import QMainWindow, QPushButton
from PyQt5 import uic

UI_PATH = "src/view/ps_view_2.ui"

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(UI_PATH, self)