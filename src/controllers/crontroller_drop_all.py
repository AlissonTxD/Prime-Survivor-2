from src.views.view_main import MainWindow
from src.models.entities.worker import WorkerThread
from src.models.model_drop_all import DropAllModel

thread = None
drop_all = None

def start_drop_all():
    try:
        global thread, drop_all
        view = MainWindow()
        view.btn_start_log_bot.setEnabled(False)
        view.btn_stop_log_bot.setEnabled(True)
        view.tooltip.tooltip("Dropa Tudo On")
        drop_all = DropAllModel()
        thread = WorkerThread(drop_all)
        drop_all.finished.connect(dropall_finished)
        thread.start()
    except Exception as e:
        print(f"[ERRO] ao iniciar Drop ALL: {e}")

def stop_dropall():
    global thread, drop_all
    if drop_all:
        drop_all.stop()
    if thread:
        thread.quit()
        thread.wait()

def dropall_finished():
    global thread, drop_all
    view = MainWindow()
    thread = None
    drop_all = None
    view.btn_start_log_bot.setEnabled(True)
    view.btn_stop_log_bot.setEnabled(False)
    view.tooltip.tooltip()




    