from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QSpinBox
from PyQt5.QtWidgets import QTabWidget, QLabel, QComboBox
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal


from src.utils import resource_path
from src.views.view_tooltip import ToolTipWindowView
from src.models.model_aim import AimModel
from src.models.entities.keyadapter import KeySequenceAdapter

UI_PATH = resource_path("src/views/ps_view_2.ui")


class MainWindow(QMainWindow):
    start_log_bot_signal = pyqtSignal()
    stop_log_bot_signal = pyqtSignal()
    save_config_signal = pyqtSignal()
    aim_signal = pyqtSignal(str)

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
            self.aim_model = AimModel()
            self.key_registry = {}

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
            self.btn_start_log_bot.clicked.connect(self.start_log_bot_signal)
            self.btn_stop_log_bot.clicked.connect(self.stop_log_bot_signal)
            self.btn_save.clicked.connect(self.save_config_signal)
            self.btn_select_color.clicked.connect(lambda: self.aim_signal.emit("select_color"))
            self.btn_activate_aim.clicked.connect(lambda: self.aim_signal.emit("aim_toggle"))
            self.spinbox_aim_size.textChanged.connect(lambda: self.aim_signal.emit("aim_update"))
            self.combobox_aim_style.currentTextChanged.connect(lambda: self.aim_signal.emit("aim_update"))
            

    def load_data_on_view(self, data):
        self.__load_key_config(data["hotkeys"])
        self.__load_aim_config(data["aim"])

    def __load_key_config(self, config):
        for sequence in self.key_list:
            try:
                if sequence["key"] in config:
                    sequence["lineedit"].setText(config[sequence["key"]])
                    self.key_registry[config[sequence["key"]]] = sequence["adapter"]
            except Exception as e:
                print(f"Erro ao carregar configurações: {e}")

    def __load_aim_config(self, config):
        try:
            if "aim_color" in config:
                cor = config["aim_color"]
                self.label_aim_color.setStyleSheet(f"background-color: rgb({cor[0]}, {cor[1]}, {cor[2]});border: 3px outset rgb(93, 49, 0);border-radius: 10px;")
                self.aim_model.color = (cor[0], cor[1], cor[2])
            if "aim_size" in config:
                self.spinbox_aim_size.setValue(config["aim_size"])
            if "aim_style" in config:
                index = self.combobox_aim_style.findText(config["aim_style"])
                if index != -1:
                    self.combobox_aim_style.setCurrentIndex(index)
        except Exception as e:
            print(f"Erro ao carregar configurações: {e}")