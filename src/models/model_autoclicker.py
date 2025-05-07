from src.models.entities.macrobase import MacroBase
from pyautogui import click
from time import sleep

class AutoClickModel(MacroBase):
    def __init__(self, deley):
        super().__init__()
        self.running = True
        self.delay = deley

    def run(self):
        self.focus_in_window()
        while self.running:
            click()
            sleep(self.delay)
        self.finished.emit()

    def stop(self):
        self.running = False
