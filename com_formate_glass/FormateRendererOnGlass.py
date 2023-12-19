import time
from datetime import datetime

from PyQt5.QtCore import QThread, pyqtSignal

from com_formate_glass.FormateRect import FormateRect
import pytesseract


from com_formate_logs.FormateLogger import FormateLogger
from com_formate_logs.FormateLogEntry import FormateLogEntry


class FormateRendererOnGlass(QThread):
    render_button_signal = pyqtSignal(FormateRect)

    def __init__(self, glass,boxes):
        super().__init__()
        self.glass = glass
        self.boxes = boxes




    def get_text_at_position(self, roi):
        start = time.time()
        text = pytesseract.image_to_string(roi, config='-l eng --oem 1 --psm 7')
        end = time.time()
        FormateLogger.log(FormateLogEntry(thread_name="FormateRendererOnGlass.py",description="Decode text from rect",rect_involved=FormateRect(text=FormateLogger.normalize_text(text)),processing_time=str(end - start)))   
        return text

    def run(self):
        FormateLogger.log(FormateLogEntry(thread_name="FormateTransparentGlass.py",description="is running"))    

