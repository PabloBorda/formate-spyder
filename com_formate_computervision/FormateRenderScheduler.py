import pyautogui
from PyQt5.QtCore import QThread, pyqtSignal, QReadWriteLock

from com_formate_glass.FormateRect import FormateRect
import time
from datetime import datetime

from com_formate_logs.FormateLogger import FormateLogger
from com_formate_logs.FormateLogEntry import FormateLogEntry


class FormateRenderScheduler(QThread):
    # Renders the elements in the screen in the best order so there is no latency for the user

    render_button_signal = pyqtSignal(FormateRect)

    def __init__(self, glass):
        super().__init__()
        self.render_scheduler = []
        self.screenshots = []

    def append(self, rect):
        self.render_scheduler.append(rect)

    def add(self, many_rects):
        self.render_scheduler = self.render_scheduler + many_rects

    def append_screenshot(self, screenshot):
        self.screenshots.append(screenshot)

    def sort_queue(self, currentMouseX, currentMouseY):
        # Schedule elements to be render closer to the mouse and prioritizing smaller screenshot crops
        self.render_scheduler = sorted(self.render_scheduler, key=lambda image_rect: (
                (abs(image_rect.x - currentMouseX) + abs(image_rect.y - currentMouseY)) + (
                (image_rect.x - image_rect.w) * (image_rect.y - image_rect.h))), reverse=False)

    def remove_elements_to_render_from_screen_changed_area(self,area_changed):
        FormateLogger.log(FormateLogEntry(thread_name="FormateRenderScheduler.py",description=("Removing buttons to render in screen changed area amount of elements" + str(len(self.render_scheduler)))))
        self.render_scheduler = [e for e in self.render_scheduler if (e.rect.x >= area_changed.x and
                                                                      e.rect.y >= area_changed.y and
                                                                      (e.rect.w <= (area_changed.w - e.rect.x)) and
                                                                      (e.rect.h <= (area_changed.h - e.rect.y)))]
        FormateLogger.log(FormateLogEntry(thread_name="FormateRenderScheduler.py",description=("Amount of Elements removed:" + str(len(self.render_scheduler)))))

    
    
    def run(self):
        #print("SCHEDULER THREAD: is running...")
        while True:
            if len(self.render_scheduler) > 0:
                old_hash = hash(str(self.render_scheduler))
                while old_hash != hash(str(self.render_scheduler)):
                    currentMouseX, currentMouseY = pyautogui.position()
                    #print("Current mouse position: " + str(currentMouseX) + "," + str(currentMouseY))
                    write_lock = QReadWriteLock()
                    write_lock.lockForWrite()
                    start = time.time()
                    self.sort_queue(currentMouseX, currentMouseY)
                    end = time.time()
                    FormateLogger.log(FormateLogEntry(thread_name="FormateRenderScheduler.py",description="Sort elements from button render queue closer to the mouse "),processing_time=str(end - start))
                    write_lock.unlock()
                    #print("SCHEDULER THREAD: Sorting buttons closer to the mouse and by smaller size" + str(self.render_scheduler))
                    old_hash = hash(str(self.render_scheduler))

    def insert_screenshot_first(self, screenshot):
        self.screenshots.insert(0, screenshot)
