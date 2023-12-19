from PIL import Image
from PyQt5.QtCore import pyqtSignal, QThread
from PIL import ImageChops  # $ pip install pillow
from PyQt5.QtGui import QPixmap, QScreen
from PyQt5.QtWidgets import QApplication
from pyscreenshot import grab  # $ pip install pyscreenshot
import time
import io
from com_formate_computervision.FormatePicture import FormatePicture
from com_formate_computervision.FormateVisionInput import FormateVisionInput
from com_formate_glass.FormateRect import FormateRect


class FormateScreenReaderPyQt5(QThread):


    def __init__(self, render_scheduler):
        super().__init__()
        self.render_scheduler = render_scheduler

    def run(self):
        print("QThread running screenreader")
        screen_size = QApplication.desktop().geometry()
        while True:
            start = time.time()
            im_pyqt5 = QScreen.grabWindow(QApplication.desktop().winId(), screen_size.x, screen_size.y, screen_size.width(), screen_size.height())
            im = io.BytesIO(im_pyqt5.data())
            im.show()
            end = time.time()
            print("Time take from FormateScreenshotReader 1: " + str(end - start))
            while True:
                start = time.time()
                current_screen = grab()
                #current_screen.show()
                diff = ImageChops.difference(im, current_screen)
                #diff.show()
                end = time.time()
                print("Time take from FormateScreenshotReader 2: " + str(end - start))

                bbox = diff.getbbox()
                if bbox is not None:  # exact comparison
                    break
            cropped_area = im.crop(bbox).convert(mode="L")
            #cropped_area.show()
            print(str(bbox))
            fp = FormateRect(bbox[0], bbox[1], bbox[2], bbox[3], t="screenshot_reader", im=cropped_area)
            print("Captured changing image crop...")
            self.render_scheduler.append_screenshot(fp)
            print("Screenshot added to scheduler for Tesseract processing...")
