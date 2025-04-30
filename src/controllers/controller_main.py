from .controller_log_bot import start_log_bot, stop_log_bot
from src.views.view_main import MainWindow


class MainController:
    def __init__(self, view: MainWindow):
        self.view = view
        view.start_log_bot_signal.connect(self.start_bot)
        view.stop_log_bot_signal.connect(self.stop_bot)

    def start_bot(self):
        start_log_bot()

    def stop_bot(self):
        stop_log_bot()
