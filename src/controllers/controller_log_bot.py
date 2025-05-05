from src.models.model_log_bot import LogBotModel
from src.models.model_image_generator import ImageGeneratorModel
from src.views.view_main import MainWindow
from src.models.entities.worker import WorkerThread

thread = None
log_bot = None


def start_log_bot(ocr, config):
    try:
        global thread, log_bot
        view = MainWindow()

        view.btn_start_log_bot.setEnabled(False)
        view.btn_start_log_bot.setText("Rodando...")
        view.btn_stop_log_bot.setEnabled(True)
        view.tooltip.tooltip("Log Bot Monitorando...")

        img_gen_model = ImageGeneratorModel(config["subimage_cut"])
        log_bot = LogBotModel(img_gen_model, ocr, config)
        thread = WorkerThread(log_bot)
        log_bot.finished.connect(bot_finished)
        thread.start()

    except Exception as e:
        print(f"[ERRO] ao iniciar Log Bot: {e}")


def stop_log_bot():
    global thread, log_bot
    if log_bot:
        log_bot.stop()
    if thread:
        thread.quit()
        thread.wait()


def bot_finished():
    global thread, log_bot
    view = MainWindow()

    thread = None
    log_bot = None

    view.btn_start_log_bot.setEnabled(True)
    view.btn_start_log_bot.setText("Iniciar Bot")
    view.btn_stop_log_bot.setEnabled(False)
    view.tooltip.tooltip()
