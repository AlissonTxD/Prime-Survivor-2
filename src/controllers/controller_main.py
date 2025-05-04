from .controller_log_bot import start_log_bot, stop_log_bot
from src.views.view_main import MainWindow
from src.models.model_ocr_loader import OCRLoader
from src.models.repository.config_json import ConfigRepository

class MainController:
    def __init__(self, view: MainWindow):
        self.view = view
        self.config = ConfigRepository()
        self.view.load_key_config(self.config.data["hotkeys"])
        self.ocr = None
        self.view.start_log_bot_signal.connect(lambda: start_log_bot(self.ocr, self.config.data["logbot"]))
        self.view.stop_log_bot_signal.connect(stop_log_bot)
        self.view.save_config_signal.connect(self.save_config)
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