#!/usr/bin/env python
# -*- coding:utf-8 -*-

import threading

class Handler(threading.Thread):
    
    def __init__(self,param1,param2):
        threading.Thread.__init__(self)
        self.param1 = param1
        self.param2 = param2


    def run(self):
        print 'Parametro 1:',self.pParam1
        print 'parametro 2:',self.pParam2
    