from PyQt5.QtWidgets import QMainWindow, QPushButton
from PyQt5 import uic

from src.utils import resource_path
from src.controllers.controller_main import MainController

UI_PATH = resource_path("src/views/ps_view_2.ui")


class MainWindow(QMainWindow):
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
            self.controller = MainController()
            uic.loadUi(UI_PATH, self)
            self.btn_iniciar_log_bot = self.findChild(
                QPushButton, "btn_iniciar_log_bot"
            )
            self.btn_iniciar_log_bot.clicked.connect(self.ativar_log_botao)

    def ativar_log_botao(self):
        self.btn_iniciar_log_bot.setEnabled(False)
        self.controller.start_bot()
