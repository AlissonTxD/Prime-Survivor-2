import time
from pyautogui import moveTo, press
from src.models.entities.macrobase import MacroBase

class DropAllModel(MacroBase):
    def __init__(self):
        super().__init__()
        self.running = True
        self.first_slot = (1245, 280)
        self.second_slot = (1340, 280)
        slot_spacing = self.second_slot[0] - self.first_slot[0]

        self.slots = [
            (self.first_slot[0] + i * slot_spacing, self.first_slot[1])
            for i in range(6)
        ]

    def run(self):
        while self.running:
            for x, y in self.slots:
                moveTo(x, y)
                if not self.running:
                    break
                press("o")
        self.finished.emit()

    def stop(self):
        self.running = False
