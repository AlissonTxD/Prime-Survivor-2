from src.models.entities.macrobase import MacroBase
import pyautogui
from time import sleep

class AutoClickModel(MacroBase):
    def __init__(self, deley: float, button: str):
        super().__init__()
        self.running = True
        self.delay = deley
        self.button = button

    def run(self):
        pyautogui.PAUSE = 0
        pyautogui.FAILSAFE = False
        self.focus_in_window()
        check_interval = 0.05
        while self.running:
            pyautogui.click(button=self.button)

            total_wait = 0
            while total_wait < self.delay and self.running:
                sleep(check_interval)
                total_wait += check_interval

        self.finished.emit()

    def stop(self):
        self.running = False
