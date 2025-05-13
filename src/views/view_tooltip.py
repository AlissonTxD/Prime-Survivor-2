from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt


class ToolTipWindowView(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet("""
            background-color: #0f0f0f;
            color: white;
            padding: 4px;
            border-radius: 4px;
            font: bold 18pt 'Arial';
        """)
        self.setWindowOpacity(0.9)
        self.hide()
        self.move(0, 0)

    def tooltip(self, text: str = ""):
        if not text.strip():
            self.hide()
            return

        self.setText(text)
        self.adjustSize()
        self.show()
        