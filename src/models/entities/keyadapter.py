from PyQt5.QtCore import QObject, QEvent, Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QLineEdit

class KeySequenceAdapter(QObject):
    def __init__(self, line_edit: QLineEdit):
        super().__init__()  # Agora herda corretamente de QObject
        self.line_edit = line_edit
        self.line_edit.installEventFilter(self)
        self.line_edit.setPlaceholderText("Pressione uma tecla")
        self._key_sequence = None

    def eventFilter(self, obj, event):
        if obj == self.line_edit and event.type() == QEvent.KeyPress:
            key = event.key()
            modifiers = event.modifiers()

            # Ignorar teclas "soltas"
            if key in (Qt.Key_Shift, Qt.Key_Control, Qt.Key_Alt, Qt.Key_Meta):
                return True

            sequence = QKeySequence(modifiers | key)
            self._key_sequence = sequence
            self.line_edit.setText(sequence.toString())
            return True  # evento tratado

        return False

    def get_key_sequence(self):
        return self._key_sequence