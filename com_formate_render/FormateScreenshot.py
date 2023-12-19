# -*- coding: utf-8 -*-

from com_formate_render.FormateElement import FormateElement
from com_formate_logs.FormateLogger import FormateLogger
from com_formate_logs.FormateLogEntry import FormateLogEntry
from com_formate_computervision.FormateTesseract import FormateTesseract
from com_formate_workerthreads.WorkerThreads import WorkerThreads
from com_formate_glass.FormateRect import FormateRect
from PyQt5 import QtCore
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PIL import Image



class FormateScreenshot(QThread):
    
    debug_image = None
    
    glass_render_this_newly_detected_element = pyqtSignal(FormateRect)
    glass_remove_elements_as_picture_from_this_screenshot_changed = pyqtSignal(str)
    
    
    def __init__(self,glass,formate_rect,parent=None):
        super().__init__()
        self.formate_rect = formate_rect
        self.glass = glass
        #WorkerThreads.add_thread(name="screenshot_for_tesseract",my_thread=self)
        self.parent = parent
        self.childs = []       #  child screenshots
        self.elements = []     #  elements detected in screenshot , text mostly in this case
        
    def push(self,child_element):
        self.childs.insert(0, child_element)
        self.setPriority(QtCore.QThread.LowPriority)
        child_element.setPriority(QtCore.QThread.HighPriority)
        
    def update_screenshot(self,formate_screenshot):
        self.childs = []
        self.elements = []
        self.glass_remove_elements_as_picture_from_this_screenshot_changed.emit('glass_remove_elements')
        self.formate_rect = formate_screenshot.formate_rect
        
        
        
    def insert_screenshot(self,formate_screenshot):
        if self.formate_rect.is_equal_to(formate_screenshot.formate_rect):
            FormateLogger.log(FormateLogEntry(thread_name="FormateScreenshot.py",description="Replace Screenshot",rect_involved=str(self.formate_rect),another_rect_involved=str(formate_screenshot.formate_rect)))
            self.update_screenshot(formate_screenshot)
        else:
            if (formate_screenshot.formate_rect.is_inside_another(self.formate_rect)):
                FormateLogger.log(FormateLogEntry(thread_name="FormateScreenshot.py",description="Adding the following screenshot as a child screenshot of the parent ",rect_involved=str(self.formate_rect),another_rect_involved=str(formate_screenshot.formate_rect)))
                if (self.debug_image == None):
                    self.debug_image = self.formate_rect.im
                else:       
                    self.debug_image = Image.blend(self.formate_rect, self.debug_image, alpha=.5)
                self.childs.append(formate_screenshot)
            else:
                FormateLogger.log(FormateLogEntry(thread_name="FormateScreenshot.py",description="going up to find parent screenshot for ",rect_involved=str(formate_screenshot.formate_rect)))
                if self.parent!=None:
                    self.parent.insert_screenshot(formate_screenshot)
                else:
                    FormateLogger.log(FormateLogEntry(thread_name="FormateScreenshot.py",description="it should not be possible but there is no parent for ",rect_involved=str(formate_screenshot.formate_rect)))
                    self.glass.root_screenshot = self
        self.debug_image.save("com_formate_logs/logs/images/debug.png")
        FormateLogger.log(FormateLogEntry(thread_name="FormateScreenshot.py",description="Blended Screenshots for Debugging ",rect_involved=str(FormateRect(im=self.debug_image,path_if_persisted="com_formate_logs/logs/images/debug.png"))))

    
    
    @QtCore.pyqtSlot(FormateRect)
    def render_element(self,element):
        self.elements.append(element)
        self.glass_render_this_newly_detected_element.emit(element)
        
    
    def run(self):
        FormateLogger.log(FormateLogEntry(thread_name="FormateScreenshot.py",description="Executing Tesseract from FormateScreenshot thread ",rect_involved=str(self.formate_rect)))
        # Create new computer vision thread to recognize image patterns
        self.processing_service = FormateTesseract(self.glass,parent=self,rect=self.formate_rect)
        self.processing_service.new_element_detected.connect(self.render_element)

        while self.processing_service.is_running_shoot():
            pass

