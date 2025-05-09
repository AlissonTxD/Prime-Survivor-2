from PyQt5.QtCore import QObject, QMetaObject, Qt, pyqtSlot
from .controller_log_bot import start_log_bot, stop_log_bot
from .controller_autoclicker import start_autoclicker, stop_autoclicker
from src.views.view_main import MainWindow
from src.models.model_ocr_loader import OCRLoader
from src.models.repository.config_json import ConfigRepository
from src.models.model_hotkeys import HotkeysModel


class MainController(QObject):
    def __init__(self, view: MainWindow):
        super().__init__()
        self.view = view
        self.config = ConfigRepository()
        self.hotkeys = HotkeysModel()
        self.view.load_key_config(self.config.data["hotkeys"])
        self.index_of_config = 2
        self.ocr = None
        self.hotkeys_isnt_activated = False
        self.something_is_running = False
        self.view.tab_widget.currentChanged.connect(self.__on_tab_changed)
        self.view.start_log_bot_signal.connect(self.start_log_bot_controller)
        self.view.stop_log_bot_signal.connect(self.stop_all_controller)
        self.view.save_config_signal.connect(self.save_config)
        self.load_hotkeys_and_callbacks()
        self.start_ocr_load()

    def start_ocr_load(self):
        self.worker = OCRLoader()
        self.worker.loaded.connect(self.on_ocr_loaded)
        self.worker.start()

    def on_ocr_loaded(self, ocr_instance):
        self.ocr = ocr_instance
        self.view.btn_start_log_bot.setText("Iniciar Bot")
        self.view.btn_start_log_bot.setEnabled(True)

    def save_config(self):
        new_config = {}
        for camp in self.view.key_list:
            line = camp["lineedit"]
            key = camp["key"]
            new_config[key] = line.text()
        self.config.data["hotkeys"] = new_config
        self.config.save_config()
        self.hotkeys.stop()
        self.config.reload_config()
        self.view.load_key_config(self.config.data["hotkeys"])
        self.view.tab_widget.setCurrentIndex(0)

    def load_hotkeys_and_callbacks(self):
        self.hotkeys_and_callbacks = {
            self.config.data["hotkeys"][
                "lineedit_input_logbot_start"
            ]: lambda: QMetaObject.invokeMethod(
                self, "start_log_bot_controller", Qt.QueuedConnection
            ),
            self.config.data["hotkeys"][
                "lineedit_input_stop"
            ]: lambda: QMetaObject.invokeMethod(
                self, "stop_all_controller", Qt.QueuedConnection
            ),
            self.config.data["hotkeys"][
                "lineedit_input_autoclick"
            ]: lambda: QMetaObject.invokeMethod(
                self, "start_autoclicker_controller", Qt.QueuedConnection
            ),
        }
        self.hotkeys.set_hotkeys(self.hotkeys_and_callbacks)

    def __on_tab_changed(self, index):
        if index == self.index_of_config:
            self.hotkeys_isnt_activated = True
            self.hotkeys.stop()
        elif index != self.index_of_config and self.hotkeys_isnt_activated:
            self.hotkeys_isnt_activated = False
            self.load_hotkeys_and_callbacks()

    @pyqtSlot()
    def start_log_bot_controller(self):
        if self.something_is_running:
            return
        else:
            self.something_is_running = True
            start_log_bot(self.ocr, self.config.data["logbot"])

    @pyqtSlot()
    def start_autoclicker_controller(self):
        if self.something_is_running:
            return
        else:
            self.something_is_running = True
            start_autoclicker()

    @pyqtSlot()
    def stop_all_controller(self):
        self.something_is_running = False
        stop_log_bot()
        stop_autoclicker()
