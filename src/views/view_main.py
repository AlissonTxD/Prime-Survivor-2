from PyQt5.QtWidgets import QMainWindow, QPushButton
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal

from src.utils import resource_path

UI_PATH = resource_path("src/views/ps_view_2.ui")


class MainWindow(QMainWindow):
    stop_log_bot = pyqtSignal()
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.initialized = False
        return cls.__instance

    def __init__(self, controller=None):
        if not self.initialized:
            super(MainWindow, self).__init__()
            self.initialized = True
            self.controller = controller
            uic.loadUi(UI_PATH, self)
            self.btn_start_log_bot = self.findChild(QPushButton, "btn_start_log_bot")
            self.btn_stop_log_bot = self.findChild(QPushButton, "btn_stop_log_bot")
            self.btn_stop_log_bot.setEnabled(False)
            self.btn_start_log_bot.clicked.connect(self.activate_logbot_button)
            self.btn_stop_log_bot.clicked.connect(self.deactivate_logbot_button)

    def activate_logbot_button(self):
        self.btn_start_log_bot.setEnabled(False)
        self.btn_stop_log_bot.setEnabled(True)
        self.btn_start_log_bot.setText("Rodando...")
        self.controller.start_bot()

    def deactivate_logbot_button(self):
        self.btn_start_log_bot.setEnabled(True)
        self.btn_stop_log_bot.setEnabled(False)
        self.btn_start_log_bot.setText("Iniciar")
        self.controller.stop_bot()