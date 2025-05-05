from PyQt5.QtCore import QThread


class WorkerThread(QThread):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def run(self):
        self.model.run()
