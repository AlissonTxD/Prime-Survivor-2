import sys
from PyQt5.QtWidgets import QApplication, QWidget, QRubberBand
from PyQt5.QtCore import Qt, QRect, QPoint, QSize
from PyQt5.QtGui import QPalette, QColor


class AreaSelector(QWidget):
    def __init__(self):
        super().__init__()

        # Remove bordas e mantém no topo
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        # Permite transparência com fundo escurecido
        self.setWindowOpacity(0.3)
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0, 100))  # levemente escuro
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Usa tela primária
        screen_geometry = QApplication.primaryScreen().geometry()
        self.setGeometry(screen_geometry)

        # Inicializa seleção
        self.origin = QPoint()
        self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)

        self.show()  # Mostra a janela ao final

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
            print(f"Área selecionada: ({rect.left()}, {rect.top()}) → ({rect.right()}, {rect.bottom()})")
            self.rubber_band.hide()
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    selector = AreaSelector()
    sys.exit(app.exec_())
