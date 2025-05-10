from src.models.model_autowalk import AutoWalkModel
from src.views.view_main import MainWindow
from src.models.entities.worker import WorkerThread

thread = None
autowalk = None

def start_autowalker():
    try:
        global thread, autowalk
        view = MainWindow()
        view.btn_start_log_bot.setEnabled(False)
        view.btn_stop_log_bot.setEnabled(True)
        view.tooltip.tooltip("Caminhar Automatico On")
        autowalk = AutoWalkModel()
        thread = WorkerThread(autowalk)
        autowalk.finished.connect(autowalker_finished)
        thread.start()
    except Exception as e:
        print(f"[ERRO] ao iniciar AutoWalk: {e}")

def stop_autowalker():
    global thread, autowalk
    if autowalk:
        autowalk.stop()
    if thread:
        thread.quit()
        thread.wait()

def autowalker_finished():
    global thread, autowalk
    view = MainWindow()
    thread = None
    autowalk = None
    view.btn_start_log_bot.setEnabled(True)
    view.btn_stop_log_bot.setEnabled(False)
    view.tooltip.tooltip()




    