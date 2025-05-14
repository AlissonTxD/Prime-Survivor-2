from collections import namedtuple

from PyQt5.QtCore import QObject, QMetaObject, Qt, pyqtSlot, QTimer
from .controller_log_bot import start_log_bot, stop_log_bot
from .controller_autoclicker import start_auto_clicker, stop_auto_clicker
from .controller_autowalker import start_auto_walker, stop_auto_walker
from .crontroller_drop_all import start_drop_all, stop_drop_all
from .controller_aim import set_aim_color, aim_update, aim_toggle
from src.views.view_main import MainWindow
from src.models.model_ocr_loader import OCRLoader
from src.models.repository.config_json import ConfigRepository
from src.models.model_hotkeys import HotkeysModel

MacroStatus = namedtuple('MacroStatus', ['active', 'name'])


class MainController(QObject):
    def __init__(self, view: MainWindow):
        super().__init__()
        self.view = view
        self.config = ConfigRepository()
        self.hotkeys = HotkeysModel()
        self.view.load_data_on_view(self.config.data)
        aim_update()
        self.index_of_config = 2
        self.ocr = None
        self.hotkeys_isnt_activated = False
        self.macro_running = MacroStatus(False, "none")
        self.view.maintab.currentChanged.connect(self.__on_tab_changed)
        self.view.start_log_bot_signal.connect(self.start_log_bot_controller)
        self.view.stop_log_bot_signal.connect(self.stop_all_controller)
        self.view.save_config_signal.connect(self.__save_config)
        self.view.aim_signal.connect(self.aim_controller)
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

# Aim Config
    def aim_controller(self, aim_config):
        if aim_config == "select_color":
            set_aim_color()
            self.aim_controller("aim_update")
        elif aim_config == "aim_update":
            config = aim_update()
            print(config)
            self.config.data["aim"] = config
            self.config.save_config()
        elif aim_config == "aim_toggle":
            aim_toggle()

# Hotkey Config
    def __save_config(self):
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
            print(f"Tab changed to {index}")
            if index == self.index_of_config:
                self.hotkeys_isnt_activated = True
                self.hotkeys.stop()
                print("Hotkeys stopped")
            elif index != self.index_of_config and self.hotkeys_isnt_activated:
                self.hotkeys_isnt_activated = False
                self.__load_hotkeys_and_callbacks()

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
