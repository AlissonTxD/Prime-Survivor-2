from src.models.model_log_bot import LogBotModel
from src.models.model_image_generator import ImageGeneratorModel
from src.views.view_main import MainWindow
from src.models.entities.worker import WorkerThread

thread = None
log_bot = None
view = None


def start_log_bot(ocr, config):
    global thread, log_bot, view
    view = MainWindow()
    img_gen_model = ImageGeneratorModel(config["subimage_cut"])
    view.btn_start_log_bot.setEnabled(False)
    view.btn_stop_log_bot.setEnabled(True)
    log_bot = LogBotModel(img_gen_model, ocr, config)
    thread = WorkerThread(log_bot)
    log_bot.finished.connect(bot_finished)
    thread.start()
    view.tooltip.tooltip("Log Bot Monitorando...")
    view.btn_start_log_bot.setText("Rodando...")


def stop_log_bot():
    print("Stopping bot...")
    if log_bot:
        log_bot.stop()
    if thread:
        thread.quit()
        thread.wait()


def bot_finished():
    global thread, log_bot, view
    thread = None
    log_bot = None
    view.btn_start_log_bot.setText("Iniciar Bot")
    view.btn_start_log_bot.setEnabled(True)
    view.btn_stop_log_bot.setEnabled(False)
    view.tooltip.tooltip()
