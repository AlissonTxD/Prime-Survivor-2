from abc import ABCMeta, abstractmethod
from PyQt5.QtCore import QObject, pyqtSignal


class MetaQObjectABC(type(QObject), ABCMeta):
    pass


class MacroBase(QObject, metaclass=MetaQObjectABC):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()

    @abstractmethod
    def run(self):
        """Obrigatório implementar nas subclasses"""
        pass

    def stop(self):
        """Pode ser sobrescrito se necessário"""
        pass
