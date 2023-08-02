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
import pathlib

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


# %% Variables

# modify path to utils and data based off cwd (run as utils or fema_cria)
if pathlib.Path.cwd().stem == "fps_server":
    path_utils = pathlib.Path("utils/")
    path_data = pathlib.Path("data/")
    path_out = pathlib.Path("output/")

elif pathlib.Path.cwd().stem == "utils":
    path_utils = pathlib.Path.cwd()
    path_data = pathlib.Path("../data/")
    path_out = pathlib.Path("../output/")

elif pathlib.Path.cwd().stem == "fps":
    path_local = pathlib.Path("fps_server/")
    path_utils = pathlib.Path(path_local / "utils/")
    path_data = pathlib.Path(path_local / "data/")
    path_out = pathlib.Path(path_local / "output/")


# %% Logger
# Create one logger:
#     - track detailed information of issues; but overwrite

# create logger
# logger = logging.getLogger(name=__name__)
logger = logging.getLogger(name=__name__)
if logger.hasHandlers():
    logger.handlers.clear()
logger.setLevel(logging.DEBUG)
logger.propagate = False

# create file handler which logs even debug messages

file_name = "fps_server.log"
fh = logging.FileHandler(path_out / file_name, mode="w")
fh.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter(
    fmt="%(asctime)s - %(module)s - " "%(levelname)s - %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
)
# add formatter to ch_issues
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add ch_issues to logger
logger.addHandler(fh)
logger.addHandler(ch)
logger.info("issues logger ready")

# troubleshooting
# loggers = [logging.getLogger()]  # get the root logger
# loggers = loggers + [logging.getLogger(name) for name in logging.root.manager.loggerDict]
