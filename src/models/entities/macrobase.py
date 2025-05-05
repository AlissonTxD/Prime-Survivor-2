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
        pass

    def stop(self):
        pass

    def focus_in_window(self, window_name) -> None:
        try:
            windows = gw.getWindowsWithTitle(window_name)
            if not windows:
                print(f"window called '{window_name}' not found.")
                return

            window = windows[0]
            if gw.getActiveWindow() != window:
                window.activate()
            else:
                print(f"window called '{window_name}' already active.")
        except Exception as e:
            print(f"Error focusing window '{window_name}': {e}")
