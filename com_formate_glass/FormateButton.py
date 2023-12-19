#!/usr/bin/python3
#-*- coding: utf-8 -*-
import random

from PyQt5.QtWidgets import QPushButton


class FormateButton:
	def __init__(self,parent):
		self.name = None
		self.parent = parent
		self.rect = None

	def __init__(self, formate_rect, parent, color=None):
		self.name = formate_rect.text
		self.parent = parent
		self.rect = formate_rect
		self.qt_button = QPushButton(self.name, parent)
		if color is None:
			r = lambda: random.randint(0, 255)
			self.qt_button.setStyleSheet("background-color: rgb(" + (str(r()) + "," + str(r()) + "," + str(r())) + ");")
		else:
			self.qt_button.setStyleSheet("background-color: rgb(" + color[0] + "," + color[1] + "," + color[2] + ");")
		font = self.qt_button.font()
		font.setPointSize(int((int(formate_rect.h) - int(formate_rect.y))/2)-4)
		self.qt_button.setFont(font)
		self.qt_button.move(int(formate_rect.x/2), int(formate_rect.y/2))
		self.qt_button.resize(int(int((formate_rect.w) - int(formate_rect.x))/2), int((int(formate_rect.h) - int(formate_rect.y))/2))
		self.qt_button.clicked.connect(self.clickButtonMethod)
		self.qt_button.show()

	def set_coordinates_width_and_height(self, formate_rect):
		self.qt_button.move(int(formate_rect.x/2), int(formate_rect.y/2))
		self.qt_button.resize(int(int((formate_rect.w) - int(formate_rect.x))/2), int((int(formate_rect.h) - int(formate_rect.y))/2))

	def get_coordinates(self):
		return self.rect


	def clickButtonMethod(self):
		print("clicked button")

	def highlight(self, ):
		pass

