# -*- coding: utf-8 -*-
from com_formate_glass.FormateRect import FormateRect

class FormateElement:
    
    def __init__(self,glass):
        self.formate_rect = None
        self.childs = []
        self.processing_thread = None
        self.glass = glass
        
        