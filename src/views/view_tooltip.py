from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt


class ToolTipWindowView(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint)
        self.setStyleSheet(
            """
            background-color: #0f0f0f;
            color: white;
            padding: 2px;
            border-radius: 3px;
            font: 87 18pt "Arial Black";
        """
        )
        self.move(0, 0)

    def tooltip(self, text: str = ""):
        if self.isVisible() and text == "" or text == "":
            self.hide()
        else:
            self.setText(text)
            self.adjustSize()
            self.show()


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    tooltip = ToolTipWindowView()
    tooltip.tooltip("Estou comendo cu de curioso")
    sys.exit(app.exec_())
