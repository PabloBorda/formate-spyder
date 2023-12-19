import datetime
import re
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
from matplotlib.pyplot import figure
import tablib

import cherrypy


class FormateLogger:
        

    @classmethod
    def enabled(cls):
        return True

    @classmethod
    def terminal_output_enabled(cls):
        return False
    
    @classmethod
    def csv_enabled(cls):
        return True
    


    @classmethod
    def log(cls, formate_log_entry):
        if FormateLogger.enabled:
            now = datetime.datetime.now()
            current_date = now.strftime("%Y_%m_%d")
            current_log_line = str(formate_log_entry)
            if FormateLogger.csv_enabled:
                cls.logfile_path = "com_formate_logs/logs/formate_log-" + current_date + ".csv"
                with open(cls.logfile_path, "a+") as log_file:
                    log_file.write(current_log_line)   
            if FormateLogger.terminal_output_enabled:
                print(current_log_line)
                

                

    @classmethod
    def generate_chart(cls):
        style.use('default')

        fig = plt.figure()
        ax1 = fig.add_subplot(1, 1, 1)

        def animate():
            now = datetime.datetime.now()
            current_date = now.strftime("%Y_%m_%d")
            logfile_path = "logs/formate_log-" + current_date + ".csv"
            graph_data = open(logfile_path, 'r').read()
            lines = graph_data.split('\n')
            xs = []
            ys = []
            for line in lines:
                if len(line) > 1:
                    exact_time, what_thread, description, time_took = line.split(',')
                    xs.append(float(time_took))
                    # ys.append(float(y))
            ax1.clear()
            ax1.plot(xs, ys)

            ani = animation.FuncAnimation(fig, animate, interval=1000)
            plt.show()

        animate()

    @classmethod
    def normalize_text(self, str):
        return re.sub(r'\W+', '', str)

    @classmethod
    def generate_chart_text(cls):

        np.random.seed(19680801)
        data = np.random.randn(2, 100)

        fig, axs = plt.subplots(2, 2, figsize=(5, 5))
        axs[0, 0].hist(data[0])
        axs[1, 0].scatter(data[0], data[1])
        axs[0, 1].plot(data[0], data[1])
        axs[1, 1].hist2d(data[0], data[1])

        plt.show()

    @classmethod
    def ticker(cls):
        now = datetime.datetime.now()
        current_date = now.strftime("%Y_%m_%d")
        logfile_path = "logs/formate_log-" + current_date + ".csv"
        graph_data = open(logfile_path, 'r').read()
        lines = graph_data.split('\n')
        data = []

        for line in lines:
            parts = line.split(",")
            if parts[0] != '':
                dat = datetime.datetime.strptime(parts[0], '%Y-%m-%d %H:%M:%S.%f')
                tim = parts[3]
                data.append((dat, tim))

        # years = mdates.YearLocator()
        # months = mdates.MonthLocator()
        # days = mdates.DayLocator()
        # hours = mdates.HourLocator()
        # mins = mdates.MinuteLocator()

        locator = mdates.AutoDateLocator()
        formatter = mdates.AutoDateFormatter(locator)
        formatter.scaled[1 / (24. * 60.)] = '%H:%M'

        fig, ax = plt.subplots()
        exec_timestampt = [x[0] for x in data]
        exec_time_took = [x[1] for x in data]
        ax.plot(exec_timestampt, exec_time_took)

        plt.show()
