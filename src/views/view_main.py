from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QSpinBox
from PyQt5.QtWidgets import QTabWidget, QLabel, QComboBox, QColorDialog, QCheckBox
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal


from src.utils import resource_path
from src.views.view_tooltip import ToolTipWindowView
from src.views.view_aim import AimWindowView
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
            self.aim_window = AimWindowView()
            self.key_registry = {}
            self.aim_color = (255, 0, 0)

            # Main Tab
            self.maintab = self.findChild(QTabWidget, "maintab")

            # Config tab
            self.btn_select_color = self.findChild(QPushButton, "btn_select_color")
            self.label_aim_color = self.findChild(QLabel, "label_aim_color")
            self.btn_activate_aim = self.findChild(QPushButton, "btn_activate_aim")
            self.combobox_aim_style = self.findChild(QComboBox, "combobox_aim_style")
            self.spinbox_aim_size = self.findChild(QSpinBox, "spinbox_aim_size")

           # Hotkey tab - estrutura declarativa
            self.hotkey_definitions = [
                ("lineedit_input_logbot", "START_LOGBOT"),
                ("lineedit_input_stop", "STOP_ALL"),
                ("lineedit_input_autoclick", "START_AUTOCLICKER"),
                ("lineedit_input_toggleaim", "TOGGLE_AIM"),
                ("lineedit_input_autowalk", "START_AUTOWALKER"),
                ("lineedit_input_dropall", "START_DROP_ALL"),
            ]

            self.key_list = []

            for object_name, config_key in self.hotkey_definitions:
                lineedit = self.findChild(QLineEdit, object_name)
                adapter = KeySequenceAdapter(lineedit, self.key_registry)
                self.key_list.append({
                    "lineedit": lineedit,
                    "key": config_key,
                    "adapter": adapter,
                })

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
            self.btn_activate_aim.clicked.connect(self.aim_toggle)
            self.spinbox_aim_size.textChanged.connect(self.aim_update)
            self.combobox_aim_style.currentTextChanged.connect(self.aim_update)
            

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
            self.aim_update()

    def aim_update(self):
        size = int(self.spinbox_aim_size.text())
        style = self.combobox_aim_style.currentText()
        self.aim_window.aim_update(style, self.aim_color, size)
    
    def aim_toggle(self):
        if self.aim_window.isVisible():
            self.btn_activate_aim.setText("Ativar Mira")
        else:
            self.btn_activate_aim.setText("Desativar Mira")
        self.aim_window.toggle()
