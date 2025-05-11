from src.models.model_autoclicker import AutoClickModel
from src.views.view_main import MainWindow
from src.models.entities.worker import WorkerThread

thread = None
autoclicker = None

def start_auto_clicker(delay: float = 0.0):
    try:
        global thread, autoclicker
        view = MainWindow()
        view.btn_start_log_bot.setEnabled(False)
        view.btn_stop_log_bot.setEnabled(True)
        view.tooltip.tooltip("Auto Clicker On")
        autoclicker = AutoClickModel(delay)
        thread = WorkerThread(autoclicker)
        autoclicker.finished.connect(autoclicker_finished)
        thread.start()
    except Exception as e:
        print(f"[ERRO] ao iniciar AutoClicker: {e}")

def stop_auto_clicker():
    global thread, autoclicker
    if autoclicker:
        autoclicker.stop()
    if thread:
        thread.quit()
        thread.wait()

def autoclicker_finished():
    global thread, autoclicker
    view = MainWindow()
    thread = None
    autoclicker = None
    view.btn_start_log_bot.setEnabled(True)
    view.btn_stop_log_bot.setEnabled(False)
    view.tooltip.tooltip()
