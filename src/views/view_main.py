import os
import json

from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QTabWidget
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal


from src.utils import resource_path
from src.views.view_tooltip import ToolTipWindowView
from src.models.entities.keyadapter import KeySequenceAdapter

UI_PATH = resource_path("src/views/ps_view_2.ui")


class MainWindow(QMainWindow):
    start_log_bot_signal = pyqtSignal()
    stop_log_bot_signal = pyqtSignal()
    save_config_signal = pyqtSignal()

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
            self.key_registry = {}

            # Main Tab
            self.tab_widget = self.findChild(QTabWidget, "maintab")
            
            # LogBot tab
            self.btn_start_log_bot = self.findChild(QPushButton, "btn_start_log_bot")
            self.btn_stop_log_bot = self.findChild(QPushButton, "btn_stop_log_bot")

            # Config tab
            self.lineedit_input_logbot_start = self.findChild(
                QLineEdit, "lineedit_input_logbot"
            )
            self.lineedit_input_stop = self.findChild(QLineEdit, "lineedit_input_stop")
            self.lineedit_input_autoclick = self.findChild(
                QLineEdit, "lineedit_input_autoclick"
            )
            self.btn_save = self.findChild(QPushButton, "btn_save")
            # Adapters
            self.keysequence_logbot_start = KeySequenceAdapter(
                self.lineedit_input_logbot_start, self.key_registry
            )
            self.keysequence_stop = KeySequenceAdapter(
                self.lineedit_input_stop, self.key_registry
            )
            self.keysequence_autoclick = KeySequenceAdapter(
                self.lineedit_input_autoclick, self.key_registry
            )

            # key list
            self.key_list = [
                {
                    "lineedit": self.lineedit_input_logbot_start,
                    "key": "lineedit_input_logbot_start",
                    "adapter": self.keysequence_logbot_start,
                },
                {
                    "lineedit": self.lineedit_input_stop,
                    "key": "lineedit_input_stop",
                    "adapter": self.keysequence_stop,
                },
                {
                    "lineedit": self.lineedit_input_autoclick,
                    "key": "lineedit_input_autoclick",
                    "adapter": self.keysequence_autoclick,
                },
            ]

            # Start state of buttons
            self.btn_stop_log_bot.setEnabled(False)
            self.btn_start_log_bot.setEnabled(False)
            self.btn_start_log_bot.setText("Carregando...")

            # Conecting signals and slots
            self.btn_start_log_bot.clicked.connect(
                lambda: self.start_log_bot_signal.emit()
            )
            self.btn_stop_log_bot.clicked.connect(
                lambda: self.stop_log_bot_signal.emit()
            )
            self.btn_save.clicked.connect(lambda: self.save_config_signal.emit())

    def load_key_config(self, config):
        for sequence in self.key_list:
            try:
                if sequence["key"] in config:
                    sequence["lineedit"].setText(config[sequence["key"]])
                    self.key_registry[config[sequence["key"]]] = sequence["adapter"]
            except Exception as e:
                print(f"Erro ao carregar configurações: {e}")
