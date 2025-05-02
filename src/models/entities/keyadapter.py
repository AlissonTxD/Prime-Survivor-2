# src/models/entities/keyadapter.py

from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import QObject, QEvent, Qt
from PyQt5.QtGui import QKeySequence


class KeySequenceAdapter(QObject):
    def __init__(self, line_edit: QLineEdit, registry: dict):
        super().__init__()
        self.line_edit = line_edit
        self._registry = registry  # Registro global de teclas
        self._key_sequence = None

        self.line_edit.installEventFilter(self)
        self.line_edit.setPlaceholderText("Pressione uma tecla")

    def eventFilter(self, obj, event):
        if obj == self.line_edit and event.type() == QEvent.KeyPress:
            key = event.key()
            modifiers = event.modifiers()

            if key in (Qt.Key_Control, Qt.Key_Shift, Qt.Key_Alt, Qt.Key_Meta):
                return True

            sequence = QKeySequence(modifiers | key)
            str_seq = sequence.toString()

            self._remove_from_registry()

            if str_seq in self._registry and self._registry[str_seq] is not self:
                outro_adapter = self._registry[str_seq]
                outro_adapter.clear()

            self._key_sequence = sequence
            self.line_edit.setText(str_seq)
            self._registry[str_seq] = self
            print(f"list of keys: {self._registry}")
            return True

        return False

    def clear(self):
        self._remove_from_registry()
        self._key_sequence = None
        self.line_edit.clear()

    def _remove_from_registry(self):
        for key, adapter in list(self._registry.items()):
            if adapter is self:
                del self._registry[key]

    def get_key_sequence(self):
        return self._key_sequence
