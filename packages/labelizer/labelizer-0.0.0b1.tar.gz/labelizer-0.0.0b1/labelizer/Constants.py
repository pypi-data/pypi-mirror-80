# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 10:36:26 2019

@author: gebha
"""
import os, sys, getpass

class Constants:
    
    if sys.platform.startswith('win'):
        PLATFORM = "WINDOWS"
    elif sys.platform.startswith('linux'):
        PLATFORM = "LINUX"
    else:
        PLATFORM = "UNKNOWN"

    if sys.platform.startswith('linux') and 'backend'==getpass.getuser():
        DEBUG = False
    else:
        DEBUG = True