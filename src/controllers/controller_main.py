from collections import namedtuple
from time import sleep

from PyQt5.QtCore import QObject, QMetaObject, Qt, pyqtSlot
from .controller_log_bot import start_log_bot, stop_log_bot
from .controller_autoclicker import start_auto_clicker, stop_auto_clicker
from .controller_autowalker import start_auto_walker, stop_auto_walker
from .crontroller_drop_all import start_drop_all, stop_drop_all
from .controller_aim import set_aim_color, aim_update, aim_toggle
from src.models.model_area_selector import AreaSelector
from src.views.view_main import MainWindow
from src.models.model_ocr_loader import OCRLoader
from src.models.repository.config_json import ConfigRepository
from src.models.model_hotkeys import HotkeysModel

MacroStatus = namedtuple('MacroStatus', ['active', 'name'])


class MainController(QObject):
    def __init__(self, view: MainWindow):
        super().__init__()
        self.view = view
        self.index_of_config = 2
        self.ocr = None
        self.hotkeys_isnt_activated = False
        self.macro_running = MacroStatus(False, "none")
        self.config = ConfigRepository()
        self.hotkeys = HotkeysModel()
        self.view.load_data_on_view(self.config.data)
        aim_update()
        self.__conect_signal()
        self.__load_hotkeys_and_callbacks()
        self.__start_ocr_load()

# OCR Starter
    def __start_ocr_load(self):
        self.worker = OCRLoader()
        self.worker.loaded.connect(self.__on_ocr_loaded)
        self.worker.start()

    def __on_ocr_loaded(self, ocr_instance):
        self.ocr = ocr_instance
        self.view.btn_start_log_bot.setText("Iniciar Bot")
        self.view.btn_start_log_bot.setEnabled(True)

    def __conect_signal(self):
        self.view.maintab.currentChanged.connect(self.__on_tab_changed)
        self.view.start_log_bot_signal.connect(self.start_log_bot_controller)
        self.view.stop_log_bot_signal.connect(self.stop_all_controller)
        self.view.save_config_signal.connect(self.__save_config_shortcuts)
        self.view.aim_signal.connect(self.aim_controller)
        self.view.get_config_signal.connect(self.__get_config_controller)
        self.view.btn_save_config.clicked.connect(self.save_configurations)


# Aim Config
    def aim_controller(self, aim_config):
        if aim_config == "select_color":
            set_aim_color()
            self.aim_controller("aim_update")
        elif aim_config == "aim_update":
            config = aim_update()
            self.config.data["aim"] = config
            self.config.save_config()
        elif aim_config == "aim_toggle":
            aim_toggle()

# Hotkey Config
    def __save_config_shortcuts(self):
        new_config = {}
        for camp in self.view.key_list:
            line = camp["lineedit"]
            key = camp["key"]
            new_config[key] = line.text()
        self.config.data["hotkeys"] = new_config
        self.config.save_config()
        self.hotkeys.stop()
        self.config.reload_config()
        self.view.load_data_on_view(self.config.data)
        self.view.maintab.setCurrentIndex(0)

    def __load_hotkeys_and_callbacks(self):
        hotkey_definitions = [
            ("START_LOGBOT", self.start_log_bot_controller),
            ("STOP_ALL", self.stop_all_controller),
            ("START_AUTOCLICKER", self.start_autoclicker_controller),
            ("TOGGLE_AIM", self.toggle_aim),
            ("START_AUTOWALKER", self.start_autowalker_controller),
            ("START_DROP_ALL", self.drop_all_controller),
        ]

        self.hotkeys_and_callbacks = {}
        for config_key, callback in hotkey_definitions:
            hotkey = self.config.data["hotkeys"].get(config_key)
            if hotkey:
                self.hotkeys_and_callbacks[hotkey] = lambda cb=callback: QMetaObject.invokeMethod(
                    self, cb.__name__, Qt.QueuedConnection
                )
        self.hotkeys.set_hotkeys(self.hotkeys_and_callbacks)

    def __on_tab_changed(self, index):
            if index == self.index_of_config:
                self.hotkeys_isnt_activated = True
                self.hotkeys.stop()
            elif index != self.index_of_config and self.hotkeys_isnt_activated:
                self.hotkeys_isnt_activated = False
                self.__load_hotkeys_and_callbacks()

    def __get_config_controller(self, config_name):
        if config_name == "log_bot_square":
            print("Log Bot Square")
            self.area_selector = AreaSelector()
            self.area_selector.final_signal.connect(self.load_square_on_view)

    def load_square_on_view(self, coord):
        self.view.lineedit_x1.setText(str(coord[0]))
        self.view.lineedit_y1.setText(str(coord[1]))
        self.view.lineedit_x2.setText(str(coord[2]))
        self.view.lineedit_y2.setText(str(coord[3]))

    def save_configurations(self):
        try:
            coord =(
                int(self.view.lineedit_x1.text()),
                int(self.view.lineedit_y1.text()),
                int(self.view.lineedit_x2.text()),
                int(self.view.lineedit_y2.text())
                )
            channel_id = int(self.view.lineedit_channel_id.text())
            whatsapp = self.view.lineedit_whatsapp.text()
            if whatsapp == "":
                whatsapp = "none"
            self.config.data["logbot"]["whatsapp"] = whatsapp
            self.config.data["logbot"]["subimage_cut"] = coord
            self.config.data["logbot"]["channel_id"] = channel_id
        except ValueError:
            self.view.popup_message("Erro", f"Preencha todos os campos corretamente.\nPreencha pelomenos as coordenadas e o ID do canal no discord.")
            return
        self.config.save_config()
        self.view.popup_message("Sucesso", "Configurações salvas com sucesso.")

# Scripts
    def __try_start(self, start_callback, stop_callback, callback_name):
        if self.macro_running.active:
            if self.macro_running.name == callback_name:
                self.macro_running = MacroStatus(False, "none")
                stop_callback()
            else:
                return
        else:
            self.macro_running = MacroStatus(True, callback_name)
            start_callback()
        
    @pyqtSlot()
    def start_log_bot_controller(self):
        if self.ocr:
            self.config.reload_config()
            self.__try_start(lambda :start_log_bot(self.ocr, self.config.data["logbot"]), stop_log_bot, "log_bot")

    @pyqtSlot()
    def start_autoclicker_controller(self):
        self.__try_start(start_auto_clicker, stop_auto_clicker, "auto_clicker")

    @pyqtSlot()
    def start_autowalker_controller(self):
        self.__try_start(start_auto_walker, stop_auto_walker, "auto_walker")
    
    @pyqtSlot()
    def drop_all_controller(self):
        self.__try_start(start_drop_all, stop_drop_all, "drop_all")
    
    @pyqtSlot()
    def toggle_aim(self):
        aim_toggle()
    
    @pyqtSlot()
    def stop_all_controller(self):
        self.macro_running = MacroStatus(False, "none")
        stop_log_bot()
        stop_auto_clicker()
        stop_auto_walker()
        stop_drop_all()
