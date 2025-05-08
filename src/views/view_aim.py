from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen
from PyQt5.QtCore import Qt, QRect
import sys

class Crosshair(QWidget):
    def __init__(self, style="circle", color=(255, 0, 0), size=10):
        super().__init__()
        self.style = style.lower()
        self.color = color
        self.size = size

        self.setFixedSize(self.size * 2, self.size * 2)

        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setFocusPolicy(Qt.NoFocus)

        screen = QApplication.primaryScreen().geometry()
        self.move(
            screen.center().x() - self.width() // 2,
            screen.center().y() - self.height() // 2
        )

        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        color = QColor(*self.color)

        if self.style == "circle":
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawEllipse(QRect(0, 0, self.width(), self.height()))
        elif self.style == "cross":
            painter.setPen(QPen(color, 2))
            w, h = self.width(), self.height()
            painter.drawLine(w // 2, 0, w // 2, h)
            painter.drawLine(0, h // 2, w, h // 2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mira = Crosshair(style="circle", color=(0, 255, 0), size=3)
    sys.exit(app.exec_())
