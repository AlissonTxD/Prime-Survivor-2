from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen
from PyQt5.QtCore import Qt, QRect
import sys

class AimWindowView(QWidget):
    def __init__(self, style="Bolinha", color=(255, 0, 0), size=6):
        super().__init__()
        self.style = style.lower()
        self.color = color
        self.size = size

        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setFocusPolicy(Qt.NoFocus)

        self.update_geometry()

    def update_geometry(self):
        self.setFixedSize(self.size * 2, self.size * 2)
        screen = QApplication.primaryScreen().geometry()
        self.move(
            screen.center().x() - self.width() // 2,
            screen.center().y() - self.height() // 2
        )

    def toggle(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()

    def aim_update(self, style=None, color=None, size=None):
        if style:
            self.style = style.lower()
        if color:
            self.color = color
        if size:
            self.size = size
            self.update_geometry()

        self.update()


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        color = QColor(*self.color)

        if self.style == "bolinha":
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawEllipse(QRect(0, 0, self.width(), self.height()))
        elif self.style == "cruz":
            painter.setPen(QPen(color, 2))
            w, h = self.width(), self.height()
            painter.drawLine(w // 2, 0, w // 2, h)
            painter.drawLine(0, h // 2, w, h // 2)
