# importing the required libraries
import threading

from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from threading import Thread
import sys
import subprocess
import json
import random
from PyQt5.QtWidgets import QPushButton
from ar_text_shooter import ARTextShooter
from ar_monitor_change_detector import ARMonitorChangeDetector


class Window(QMainWindow):

    def initialize_screen_monitor(self):
        self.screen_monitor.monitor_screen(self)

    def initialize_mouse_monitor(self):
        self.mouse_around_area_updater.shoot_around_mouse(self)

    def __init__(self, w, h):
        super().__init__()
        # set the title

        self.screenshooter_last_output = ""
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.X11BypassWindowManagerHint
        )

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # self.setWindowFlags(QtCore.Qt.WindowTransparentForInput)

        # setting  the geometry of window 
        self.setGeometry(
            QtWidgets.QStyle.alignedRect(
                QtCore.Qt.LeftToRight, QtCore.Qt.AlignCenter,
                QtCore.QSize(w, h),
                QtWidgets.qApp.desktop().availableGeometry()
            ))

        # show all the widgets
        self.screen_monitor = ARMonitorChangeDetector()
        screen_monitor_thread = threading.Thread(target=self.initialize_screen_monitor, daemon=True)
        screen_monitor_thread.start()

        self.mouse_around_area_updater = ARTextShooter()
        mouse_monitor_thread = threading.Thread(target=self.initialize_mouse_monitor, daemon=True)
        mouse_monitor_thread.start()

        self.show()

    def buttonize(self, content_to_buttonize):
        self.screenshooter_last_output = content_to_buttonize
        self.update()

    def paintEvent(self, event):

        global button_references
        print("refresh")
        # print("Screenshooter last output:"+screenshooter_last_output)

        # delete buttons from previous text shot
        for b in button_references:
            print("Delete object " + b.text() + " of type " + type(b()))
            b.setParent(None)
            b.deleteLater()

        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 1, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.transparent, Qt.SolidPattern))
        if self.screenshooter_last_output != "":
            screenshooter_last_output_parsed = json.loads(self.screenshooter_last_output)
            for word in screenshooter_last_output_parsed:
                # print("Position: "+str(word[0]))
                pybutton = QPushButton(word[1], self)
                r = lambda: random.randint(0, 255)
                pybutton.setStyleSheet(
                    "background-color: rgb(" + (str(r()) + "," + str(r()) + "," + str(r())) + ");opacity:0.2;")
                # pybutton.setStyleSheet("margin:0px;")
                pybutton.move(int(word[0][0]), int(word[0][1]))
                pybutton.resize((int(word[0][2] / 2) - int(word[0][0] / 2)),
                                (int(word[0][3] / 2) - int(word[0][1] / 2)))
                pybutton.clicked.connect(self.clickButtonMethod)
                pybutton.show()
                button_references.append(pybutton)

            # painter.drawRect(word[0][0]-25,word[0][1]-85,word[0][2]-word[0][0]-20,word[0][3]-word[0][1]-20)
            # print("Word: "+str(word[1]))
            # painter.drawText(word[0][0]-25,word[0][1]-85,word[1])
        self.screenshooter_last_output = ""
        button_references = []

    def clickButtonMethod(self):
        print("Button Clicked")


def settings_dialog():
    print("Settings clicked...")


button_references = []

# create pyqt5 app
App = QApplication(sys.argv)

# Adding an icon 
icon = QIcon("formate.png")

# Adding item on the menu bar 
tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)

# Creating the options 
menu = QMenu()
settings_menu_item = QAction("ForMate Settings...")
settings_menu_item.triggered.connect(settings_dialog)
menu.addAction(settings_menu_item)

# To quit the app 
quit = QAction("Quit")
quit.triggered.connect(App.quit)
menu.addAction(quit)

# Adding options to the System Tray 
tray.setContextMenu(menu)

# Get current screen size
screen = App.primaryScreen()
print('Screen: %s' % screen.name())
size = screen.size()
print('Size: %d x %d' % (size.width(), size.height()))
rect = screen.availableGeometry()
print('Available: %d x %d' % (rect.width(), rect.height()))

# create the instance of our Window
window = Window(size.width(), size.height())

# start the app
sys.exit(App.exec())
