from PyQt5.QtCore import QThread, pyqtSignal


class OCRLoader(QThread):
    loaded = pyqtSignal(object)

    def run(self):
        try:
            from paddleocr import PaddleOCR
            ocr = PaddleOCR(use_angle_cls=True, lang="en")
            self.loaded.emit(ocr)
        except Exception as e:
            print(f"Error loading PaddleOCR: {e}")
