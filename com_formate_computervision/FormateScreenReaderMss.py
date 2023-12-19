import numpy
from PIL import Image
from PyQt5.QtCore import pyqtSignal, QThread
from PIL import ImageChops  # $ pip install pillow
from PyQt5.QtGui import QPixmap, QScreen
from PyQt5.QtWidgets import QApplication
from pyscreenshot import grab  # $ pip install pyscreenshot
import time
import io
import mss
from com_formate_glass.FormateRect import FormateRect
from datetime import datetime
from com_formate_render.FormateScreenshot import FormateScreenshot
from com_formate_computervision.FormateTesseract import FormateTesseract

from com_formate_logs.FormateLogger import FormateLogger
from com_formate_logs.FormateLogEntry import FormateLogEntry
from com_formate_workerthreads.WorkerThreads import WorkerThreads
from datetime import datetime

class FormateScreenReaderMss(QThread):
    
    changedPixels = pyqtSignal(FormateScreenshot)

    def __init__(self, glass=None):
        super().__init__()
        self.glass = glass
        self.desktop_size = QApplication.desktop().geometry()
     
        self.datetimeObject = None


    def screenshot(self):
        with mss.mss() as mss_instance:
            monitor = mss_instance.monitors[0]
            im_mss = mss_instance.grab(monitor)
        im_mss_arr = numpy.asarray(im_mss)
        im = Image.fromarray(im_mss_arr)
        return im

    def run(self):

        while True:
            start = time.time()
            im = self.screenshot().convert(mode="L")
            im_width, im_height = im.size
            self.datetimeObject = datetime.now()
            p = "com_formate_logs/logs/images/" + self.datetimeObject.strftime('%Y%m%d%H%M%S') + "_a.png"
            im.save(p)
            end = time.time()
            fp = FormateRect(0,0, im_width, im_height, t="screenshot_reader", im=im.convert(mode="L"),path_if_persisted=p)
            FormateLogger.log(FormateLogEntry(thread_name="FormateScreenReaderMss.py",description="Time take from FormateScreenshotReader 1",processing_time=str(end - start),rect_involved=fp))

            
            if (self.glass.has_root_screenshot()==None):
                self.glass.root_screenshot = FormateScreenshot(self.glass,fp)
                self.changedPixels.emit(self.glass.root_screenshot)
            else:
                sh = FormateScreenshot(self.glass,fp)
                self.changedPixels.emit(sh)

            #im.show()
            while True:
                start = time.time()
                current_screen = self.screenshot().convert(mode="L")
                p1 = "com_formate_logs/logs/images/" + self.datetimeObject.strftime('%Y%m%d%H%M%S') + "_b.png"
                current_screen.save(p1)
                #im.show()
                #current_screen.show()
                diff = ImageChops.difference(im, current_screen)
                #diff.show()
                p2 = "com_formate_logs/logs/images/" + self.datetimeObject.strftime('%Y%m%d%H%M%S') + "_c.png"
                diff.save(p2)
                end = time.time()
                bbox = diff.getbbox()
                self.sleep(3)
                if bbox is not None:  # exact comparison
                    break
            cropped_area = im.crop(bbox).convert(mode="L")
            p3 = "com_formate_logs/logs/images/" + self.datetimeObject.strftime('%Y%m%d%H%M%S') + "_d.png"
            cropped_area.save(p3)
            fp1 = FormateRect(bbox[0], bbox[1], bbox[2], bbox[3], t="screenshot_reader", im=cropped_area,path_if_persisted=p3)
            FormateLogger.log(FormateLogEntry(thread_name="FormateScreenReaderMss.py",description="Time take from FormateScreenshotReader 2",processing_time=str(end - start),rect_involved=fp1))
            sh1 = FormateScreenshot(self.glass, fp1)
            self.changedPixels.emit(sh1)
            FormateLogger.log(FormateLogEntry(thread_name="FormateScreenReaderMss.py",description="Screen change detection",rect_involved=str(fp)))


