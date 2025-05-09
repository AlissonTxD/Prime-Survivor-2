import os
import json

from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QSpinBox
from PyQt5.QtWidgets import QTabWidget, QLabel, QComboBox, QColorDialog
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
    toggle_aim_signal = pyqtSignal(str, tuple, int)

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
            self.aim_color = (255, 0, 0)

            # Main Tab
            self.tab_widget = self.findChild(QTabWidget, "maintab")

            # Config tab
            self.btn_select_color = self.findChild(QPushButton, "btn_select_color")
            self.label_aim_color = self.findChild(QLabel, "label_aim_color")
            self.btn_activate_aim = self.findChild(QPushButton, "btn_activate_aim")
            self.combobox_aim_style = self.findChild(QComboBox, "combobox_aim_style")
            self.spinbox_aim_size = self.findChild(QSpinBox, "spinbox_aim_size")

            # LogBot tab
            self.btn_start_log_bot = self.findChild(QPushButton, "btn_start_log_bot")
            self.btn_stop_log_bot = self.findChild(QPushButton, "btn_stop_log_bot")

            # Hotket tab
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
            self.btn_select_color.clicked.connect(self.set_aim_color)
            self.btn_activate_aim.clicked.connect(self.toggle_aim)

    def load_key_config(self, config):
        for sequence in self.key_list:
            try:
                if sequence["key"] in config:
                    sequence["lineedit"].setText(config[sequence["key"]])
                    self.key_registry[config[sequence["key"]]] = sequence["adapter"]
            except Exception as e:
                print(f"Erro ao carregar configurações: {e}")

    def set_aim_color(self):
        cor = QColorDialog.getColor()
        if cor.isValid():
            self.aim_color = (cor.red(), cor.green(), cor.blue())
            self.label_aim_color.setStyleSheet(
                f"background-color: rgb({cor.red()}, {cor.green()}, {cor.blue()});border: 3px outset rgb(93, 49, 0);border-radius: 10px;")
            
    def toggle_aim(self):
        size = int(self.spinbox_aim_size.text())
        style = self.combobox_aim_style.currentText()
        self.toggle_aim_signal.emit(style, self.aim_color, size)        