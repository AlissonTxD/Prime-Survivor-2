from PyQt5.QtCore import QThread, pyqtSignal


class OCRLoader(QThread):
    loaded = pyqtSignal(object)
    error = pyqtSignal(str)

    def run(self):
        try:
            from paddleocr import PaddleOCR
            ocr = PaddleOCR(use_angle_cls=True, lang="pt")
            self.loaded.emit(ocr)
        except Exception as e:
            self.error.emit(f"Erro ao carregar OCR: {str(e)}")
