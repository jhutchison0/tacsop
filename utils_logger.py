#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
Created on 1 Oct 2020


"""

# %% Packages

import datetime
# import json
import logging
import os
# import pandas as pd
# import sys
# import time


# %% Notes

# =============================================================================
# Level     Numeric value	    When it's Used
# CRITICAL  50	A serious error, indicating that the program itself may be 
#                     unable to continue running.
# ERROR	    40	Due to a more serious problem, the software has not been 
#                     able to perform some function.
# WARNING	30	An indication that something unexpected happened, or 
#                     indicative of some problem in the near future 
#                     (e.g. ‘disk space low’). The software is still 
#                     working as expected.
# INFO	    20	Confirmation that things are working as expected.
# DEBUG	    10	Detailed information, typically of interest only 
#                     when diagnosing problems.
# NOTSET	 0	
# =============================================================================



# %% Logger

path_home = os.getcwd()
path_log = path_home + "\outputs"
file_name = path_log + "\cet_record"
# create logger
logger = logging.getLogger(name="cet_logger")
if (logger.hasHandlers()):
    logger.handlers.clear()
logger.setLevel(logging.DEBUG)
logger.propagate = True

# Timed rotating File Handler
# filename is 'string.log' with '%Y-%m-%d_%H-%M-%S' appended to end

# for Sunday rollover, need to 'discover' most recent Sunday
today = datetime.date.today()
# datetime returns 0 for Monday; shift index to 0 on Sunday
# Mon = 0,..., Sun = 6 --> Mon = 0,..Sat = 6
weekday_shift = (today.weekday() + 1) % 7
sunday = today - datetime.timedelta(weekday_shift)
# Append weekday to filename
file_name_weekly = file_name + "_" + str(sunday) + ".log"
# create a light and detailed handler
# rotate records on Sunday, W6

fh_record = logging.FileHandler(filename=file_name_weekly,
                                mode="a")
#fh_record = logging.FileHandler('cluster_method_record.log',mode = 'a')
fh_record.setLevel(logging.INFO)
fh_issues = logging.FileHandler(file_name + "_issues.log", mode="w")
fh_issues.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter(fmt="%(asctime)s - %(name)s - "\
                              "%(levelname)s - %(message)s",
                              datefmt='%Y/%m/%d %H:%M:%S')

# add formatter to both handlers
fh_record.setFormatter(formatter)
fh_issues.setFormatter(formatter)

# add ch to logger
logger.addHandler(fh_record)
logger.addHandler(fh_issues)

logger.debug('how about now, or now?')
