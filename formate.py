

from com_formate_app.FormateApp import FormateApp
from com_formate_logs.FormateLogger import FormateLogger
from com_formate_logs.FormateLogEntry import FormateLogEntry

app = FormateApp()
FormateLogger.log(FormateLogEntry(thread_name="formate.py",description="Main app running"))
print("Executing Formate..."+str(app))

