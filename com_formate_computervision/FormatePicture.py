#!/usr/bin/python3
# -*- coding: utf-8 -*-

from com_formate_computervision.FormateVisionInput import FormateVisionInput


class FormatePicture(FormateVisionInput):

    def __init__(self, formate_rect):
        self.formate_rect = formate_rect

    def to_formate_rect(self):
        return self.formate_rect
