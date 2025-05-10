from pyautogui import keyDown, keyUp
from time import sleep

from src.models.entities.macrobase import MacroBase

class AutoWalkModel(MacroBase):
    def __init__(self):
        super().__init__()
        self.running = True
        pass
    
    def run(self):
        self.focus_in_window()
        while self.running:
            keyDown("w")
            sleep(0.1)
        keyUp("w")
        self.finished.emit()
            
    def stop(self):
        self.running = False
