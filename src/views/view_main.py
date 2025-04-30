from PyQt5.QtWidgets import QMainWindow, QPushButton
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal

from src.utils import resource_path
from src.views.view_tooltip import ToolTipWindowView

UI_PATH = resource_path("src/views/ps_view_2.ui")


class MainWindow(QMainWindow):
    start_log_bot_signal = pyqtSignal()
    stop_log_bot_signal = pyqtSignal()

    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.initialized = False
        return cls.__instance

    def __init__(self):
        if not self.initialized:
            super(MainWindow, self).__init__()
            self.initialized = True
            uic.loadUi(UI_PATH, self)
            self.tooltip = ToolTipWindowView()
            self.btn_start_log_bot = self.findChild(QPushButton, "btn_start_log_bot")
            self.btn_stop_log_bot = self.findChild(QPushButton, "btn_stop_log_bot")
            self.btn_stop_log_bot.setEnabled(False)
            self.btn_start_log_bot.setEnabled(False)
            self.btn_start_log_bot.setText("Carregando...")

            self.btn_start_log_bot.clicked.connect(
                lambda: self.start_log_bot_signal.emit()
            )
            self.btn_stop_log_bot.clicked.connect(
                lambda: self.stop_log_bot_signal.emit()
            )
