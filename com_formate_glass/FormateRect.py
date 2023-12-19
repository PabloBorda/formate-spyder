#!/usr/bin/python3
#-*- coding: utf-8 -*-


class FormateRect:
    
    
    
    def __init__(self):
        self.x = "0"
        self.y = "0"
        self.w = "0"
        self.h = "0"
        self.text = "None"
        self.im = "None"
        self.path="None"

    def __init__(self, x="0", y="0", w="0", h="0", t="None", im=None,path_if_persisted="None"):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = t
        self.im = im
        self.path = path_if_persisted
        if (self.path=="None"):
            self.path = "None"
        else:
            self.path = path_if_persisted
        
    
    def is_inside_another(self,formate_rect):
        return (self.x >= formate_rect.x and
                self.y >= formate_rect.y and
                (self.w <= (formate_rect.w - self.x)) and
                (self.h <= (formate_rect.h - self.y)))
    
    def is_equal_to(self,another_rect):
        return (self.x == another_rect.x and
                self.y == another_rect.y and
                self.w == another_rect.w and
                self.h == another_rect.h)
    
    def im_html_tag_from_image_url(self,url):
        full_url = "/images/" + str(url)
        return "<a href=\"" + str(full_url) + "\"><img src=\"" + str(full_url) + "\" width=\"400px\"></a>"
    
    def __str__(self):
        if (self.im!=None):
            return self.im_html_tag_from_image_url(self.path) + "," + str(self.text) + "," + str(self.x) + "," + str(self.y) + "," + str(self.w) + "," + str(self.h)
        else:
            return "None," + str(self.text) + "," + str(self.x) + "," + str(self.y) + "," + str(self.w) + "," + str(self.h)
            

   # def to_str(self):
   #     if (self.path!=""):
   #         link = "file:///Users/goldenthinker/Projects/formate-spyder/" + self.path
   #     else:
   #         link = "nolink"
   #     print(link)
   #     return "[" + str(self.text) + "_" + str(self.x) + "_" + str(self.y) + "_" + str(self.w) + "_" + str(self.h) + "]"