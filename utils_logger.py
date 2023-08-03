#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-
"""
Updated on 2 Aug 2023


"""

# %% Packages
""" Third party and local imports """

import datetime

# import json
import logging
import os
import pathlib

# import pandas as pd
# import sys
# import time

# Local import
from utils_references import paths


# %% Notes
""" Notes from the docs on logger levels """

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


# %% Variables
""" Set script (global) variables """

path_out = paths["logs"]


# %% Logger
""" Create and customize logger """

# create logger
logger = logging.getLogger(name=__name__)
if logger.hasHandlers():
    logger.handlers.clear()
logger.setLevel(logging.DEBUG)
logger.propagate = False

# create file handler which logs even debug messages

file_name = "daily_wod"

# Timed rotating File Handler
# filename is 'string.log' with '%Y-%m-%d_%H-%M-%S' appended to end

# for Sunday rollover, need to identify most recent Sunday
today = datetime.date.today()
# datetime returns 0 for Monday; shift index to 0 on Sunday
# Mon = 0,..., Sun = 6 --> Mon = 0,..Sat = 6
weekday_shift = (today.weekday() + 1) % 7
sunday = today - datetime.timedelta(weekday_shift)
# Append weekday to filename
file_name_weekly = f"{file_name}_{sunday}"
# create a light and detailed handler
# rotate records on Sunday, W6

fh_record = logging.FileHandler(filename=path_out / f"{file_name_weekly}.log", mode="a")
fh_record.setLevel(logging.INFO)

fh_issues = logging.FileHandler(path_out / f"{file_name}.log", mode="w")
fh_issues.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter(
    fmt="%(asctime)s - %(module)s - " "%(levelname)s - %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
)

# add formatter to ch_issues
fh_record.setFormatter(formatter)
fh_issues.setFormatter(formatter)
ch.setFormatter(formatter)

# add ch_issues to logger
logger.addHandler(fh_record)
logger.addHandler(fh_issues)
logger.addHandler(ch)

# %% Troubleshoot
""" Troubleshooting and old code """

loggers = [logging.getLogger()]  # get the root logger
loggers = loggers + [
    logging.getLogger(name) for name in logging.root.manager.loggerDict
]


# %% Main
""" Display task data """

if __name__ == "__main__":
    logger.info("logger ready")


# %%
