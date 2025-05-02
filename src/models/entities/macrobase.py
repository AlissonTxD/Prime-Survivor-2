from abc import ABCMeta, abstractmethod
from PyQt5.QtCore import QObject, pyqtSignal
import pygetwindow as gw


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
    
    def focus_in_window(self, window_name) -> None:
        try:
            window = gw.getWindowsWithTitle(window_name)[0]
            window.activate()
        except IndexError:
            print(f"Janela com o título '{window_name}' não encontrada.")
        except Exception as e:
            print(f"Erro ao focar na janela: {e}")
