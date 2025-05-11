from PyQt5.QtWidgets import QColorDialog
from src.views.view_main import MainWindow

def set_aim_color():
    view = MainWindow()
    cor = QColorDialog.getColor()
    if cor.isValid():
        view.aim_model.color = (cor.red(), cor.green(), cor.blue())
        view.label_aim_color.setStyleSheet(
            f"background-color: rgb({cor.red()}, {cor.green()}, {cor.blue()});border: 3px outset rgb(93, 49, 0);border-radius: 10px;")

def aim_update():
    view = MainWindow()
    size = int(view.spinbox_aim_size.text())
    style = view.combobox_aim_style.currentText()
    view.aim_model.aim_update(style, view.aim_model.color, size)
    return style, view.aim_model.color, size
    
def aim_toggle():
    view = MainWindow()
    if view.aim_model.isVisible():
        view.btn_activate_aim.setText("Ativar Mira")
    else:
        view.btn_activate_aim.setText("Desativar Mira")
    view.aim_model.toggle()