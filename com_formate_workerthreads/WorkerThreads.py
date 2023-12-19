# -*- coding: utf-8 -*-

class WorkerThreads:
    
    give_me_thread = dict()
    
    @classmethod
    def get_thread(cls,name):
        return WorkerThreads.give_me_thread.get(name)
    
    @classmethod
    def add_thread(cls,name=None,my_thread=None):
        WorkerThreads.give_me_thread[name] = my_thread

    