# -*- coding: utf-8 -*-
import tablib
import cherrypy
import datetime
import os
import os.path
import CherrypyMako


CherrypyMako.setup()
root_dir = os.path.abspath( os.path.dirname(__file__))

class FormateLogBrowser(object):
    
    def __init__(self):
        self.data = tablib.Dataset()
        now = datetime.datetime.now()
        current_date = now.strftime("%Y_%m_%d")
        logfile_csv = "logs/formate_log-" + current_date + ".csv"
        #logfile_csv = "logs/formate_log-" + "2021_03_28" + ".csv"
        with open(logfile_csv, "r") as log_file:
            self.imported_data = self.data.load(log_file, format="csv")
        self.imported_data.headers=['TimeStamp', 'ThreadName', 'Description','Image','Text','x','y','w','h','Image_1','Text_1','x_1','y_1','w_1','h_1','Time']

    
    @cherrypy.expose
    @cherrypy.tools.mako(filename='log_browser.html')
    def index(self):
        return {'logTable':(str(self.imported_data.export("html")))}
    
    

cherrypy.config.update({'server.socket_host': '0.0.0.0',
                         'server.socket_port'  : 80,
                         'tools.mako.directories' : [os.path.join(root_dir,'browser')]})



cherrypy.quickstart(FormateLogBrowser(),'/','FormateLogBrowser.config')
