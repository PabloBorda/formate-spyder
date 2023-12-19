# -*- coding: utf-8 -*-

import datetime
from com_formate_glass.FormateRect import FormateRect

class FormateLogEntry:
    
    def __init__(self,thread_name="None",description="None",rect_involved=FormateRect(),another_rect_involved=FormateRect(),processing_time="0"):
        self.current_time = (datetime.datetime.now()).strftime("%Y%m%d%H%M%S")
        self.thread_name = thread_name
        self.description = description
        self.rect_involved = rect_involved
        self.another_rect_involved = another_rect_involved
        self.processing_time = processing_time

        
    def __str__(self):
        return str(self.current_time) + "," + str(self.thread_name) + "," + str(self.description) + "," + str(self.rect_involved) + "," + str(self.another_rect_involved) + "," + str(self.processing_time) + '\n'