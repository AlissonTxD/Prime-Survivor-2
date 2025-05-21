import sys
from PyQt5.QtWidgets import QApplication, QWidget, QRubberBand
from PyQt5.QtCore import Qt, QRect, QPoint, QSize, pyqtSignal
from PyQt5.QtGui import QPalette, QColor


class AreaSelector(QWidget):
    final_signal = pyqtSignal(tuple)
    def __init__(self):
        super().__init__()
        self.coord = None

        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        self.setWindowOpacity(0.3)
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0, 100))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        screen_geometry = QApplication.primaryScreen().geometry()
        self.setGeometry(screen_geometry)

        self.origin = QPoint()
        self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)

        self.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.origin = event.pos()
            self.rubber_band.setGeometry(QRect(self.origin, QSize()))
            self.rubber_band.show()

    def mouseMoveEvent(self, event):
        if self.rubber_band.isVisible():
            rect = QRect(self.origin, event.pos()).normalized()
            self.rubber_band.setGeometry(rect)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            rect = self.rubber_band.geometry()
            self.coord = (rect.left(), rect.top(), rect.right(), rect.bottom())
            self.rubber_band.hide()
            self.close()
            self.final_signal.emit(self.coord)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    selector = AreaSelector()
    sys.exit(app.exec_())
