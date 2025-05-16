from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QSpinBox, QMessageBox
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
            self.key_list = []
            self.hotkey_definitions = [
                ("lineedit_input_logbot", "START_LOGBOT"),
                ("lineedit_input_stop", "STOP_ALL"),
                ("lineedit_input_autoclick", "START_AUTOCLICKER"),
                ("lineedit_input_toggleaim", "TOGGLE_AIM"),
                ("lineedit_input_autowalk", "START_AUTOWALKER"),
                ("lineedit_input_dropall", "START_DROP_ALL"),
            ]
            self.__load_widgets()
            self.__configure_hotkey_handlers()
            self.__connect_signals()
            # Start state of buttons
            self.btn_stop_log_bot.setEnabled(False)
            self.btn_start_log_bot.setEnabled(False)
            self.btn_start_log_bot.setText("Carregando...")

    def __load_widgets(self):
        self.maintab = self.findChild(QTabWidget, "maintab")
        self.btn_select_color = self.findChild(QPushButton, "btn_select_color")
        self.label_aim_color = self.findChild(QLabel, "label_aim_color")
        self.btn_activate_aim = self.findChild(QPushButton, "btn_activate_aim")
        self.combobox_aim_style = self.findChild(QComboBox, "combobox_aim_style")
        self.spinbox_aim_size = self.findChild(QSpinBox, "spinbox_aim_size")
        
    def __configure_hotkey_handlers(self):
        for object_name, config_key in self.hotkey_definitions:
            lineedit = self.findChild(QLineEdit, object_name)
            adapter = KeySequenceAdapter(lineedit, self.key_registry)
            self.key_list.append({
                "lineedit": lineedit,
                "key": config_key,
                "adapter": adapter,
            })

    def __connect_signals(self):
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

    def popup_message(self, title: str = "Titulo", msg: str = "", type: str = "information"):
        if hasattr(self, "_erro_aberto") and self._erro_aberto:
            return

        msgbox = QMessageBox(self)
        msgbox.setWindowTitle(title)
        msgbox.setText(msg)
        if type == "information":
            msgbox.setIcon(QMessageBox.Information)
        elif type == "warning":
            msgbox.setIcon(QMessageBox.Warning)
        elif type == "critical":
            msgbox.setIcon(QMessageBox.Critical)
            
        msgbox.setStyleSheet("""
            QLabel {
                color: rgb(255, 137, 1);
                font-size: 14pt;
            }
            QPushButton{
            min-width: 80px;
            font-size: 12pt;
            background-color: rgb(255, 137, 1);
            border: 3px outset rgb(93, 49, 0);
            border-radius: 10px;
            color: rgb(15, 15, 15);
            }
            QPushButton:hover{
            color: rgb(255, 17, 0);
            background-color: rgb(215, 97, 0);
            }

            QPushButton:pressed{
            border: 3px inset rgb(93, 49, 0);
            color: rgb(15, 15, 15);
            background-color: rgb(255, 17, 0);
            }

            QPushButton:disabled {
            background-color: #cccccc;
            border: 2px solid #999999;
            color: #666666;
            }

        """)

        self._erro_aberto = True
        msgbox.exec_()
        self._erro_aberto = False
