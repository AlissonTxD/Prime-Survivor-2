from src.models.model_autoclicker import AutoClickModel
from src.views.view_main import MainWindow
from src.models.entities.worker import WorkerThread

thread = None
autoclicker = None

def start_auto_clicker():
    try:
        global thread, autoclicker
        view = MainWindow()
        view.btn_start_log_bot.setEnabled(False)
        view.btn_stop_log_bot.setEnabled(True)
        deley, button = get_view_data()
        view.tooltip.tooltip("Auto Clicker On")
        autoclicker = AutoClickModel(deley, button)
        thread = WorkerThread(autoclicker)
        autoclicker.finished.connect(autoclicker_finished)
        thread.start()
    except Exception as e:
        print(f"[ERRO] ao iniciar AutoClicker: {e}")

def get_view_data():
    view = MainWindow()
    try:
        delay = float(view.lineedit_deley.text()) / 1000
        if delay < 0.050:
            delay = 0.050
            view.lineedit_deley.setText("50")               
    except ValueError:
        delay = 0.1
        view.lineedit_deley.setText("100")
    if view.radiobutton_left.isChecked():
        button = "left"
    elif view.radiobutton_right.isChecked():
        button = "right"
    else:
        button = "left"
    return delay, button

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
