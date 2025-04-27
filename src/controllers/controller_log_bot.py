from PyQt5.QtCore import QThread

from src.models.model_log_bot import LogBotModel


class WorkerThread(QThread):
    def __init__(self, log_bot_model):
        super().__init__()
        self.log_bot_model = log_bot_model

    def run(self):
        self.log_bot_model.run()


thread = None
log_bot = None


def start_log_bot():
    global thread, log_bot
    log_bot = LogBotModel()
    thread = WorkerThread(log_bot)
    log_bot.finished.connect(bot_finished)
    thread.start()


def stop_log_bot():
    if log_bot:
        log_bot.stop()
    if thread:
        thread.quit()
        thread.wait()


def bot_finished():
    from src.views.view_main import MainWindow

    view = MainWindow()
    global thread, log_bot
    thread = None
    log_bot = None
    view.btn_iniciar_log_bot.setEnabled(True)
