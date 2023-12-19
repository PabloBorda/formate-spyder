from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication

import sys

from com_formate_glass.FormateTransparentGlass import FormateTransparentGlass
from com_formate_logs.FormateLogger import FormateLogger
from com_formate_computervision.FormateScreenReaderMss import FormateScreenReaderMss


class FormateApp:
    

    glass = None

    def __init__(self):


        App = QApplication(sys.argv)
        
        # Adding an icon
        self.icon = QIcon("formate.png")

        # Adding item on the menu bar
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.icon)
        self.tray.setVisible(True)

        # Creating the options
        self.menu = QMenu()
        self.settings_menu_item = QAction("ForMate Settings...")
        self.settings_menu_item.triggered.connect(self.settings_dialog)
        self. menu.addAction(self.settings_menu_item)

        # To quit the app
        self.quit = QAction("Quit")
        self.quit.triggered.connect(App.quit)
        self.menu.addAction(self.quit)

        # Adding options to the System Tray
        self.tray.setContextMenu(self.menu)

        # create the instance of our Glass implemented using a Qt transparent window
        
        self.transparent_glass = FormateTransparentGlass()
        

        # start the app
        sys.exit(App.exec())

    def settings_dialog(self):
        FormateLogger.log(FormateLogEntry(thread_name="FormateApp.py",description="Settings Dialog Selected"))    


