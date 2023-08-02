# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 09:00:00 2023

@author: jhutchison

"""

# %% Packages
""" Third party and local imports """

import pathlib
import sys

# Local import
from utils.utils_logger import logger


# %% Functions
""" Define functions """


# %% Variables
""" Set script (global) variables """

# Local paths
# modify path to utils and data based off cwd (run as utils or fps_server)
if pathlib.Path.cwd().stem == "fps_server":
    path_local = pathlib.Path.cwd()

elif pathlib.Path.cwd().stem == "utils":
    path_local = pathlib.Path("../")

elif pathlib.Path.cwd().stem == "fps":
    path_local = pathlib.Path("fps_server/")

path_data = path_local / pathlib.Path("data/")
path_logs = path_data / pathlib.Path("logs/")
path_out = path_local / pathlib.Path("output/")
path_utils = path_local / pathlib.Path("utils/")

# Ensure cross-package access by modifying path
if ".." not in sys.path:
    sys.path.insert(0, "..")

# External paths
path_fps = path_local.parent

path_tide = path_fps / pathlib.Path("./fps_tide/")
path_tide_data = path_tide / pathlib.Path("data/")

path_dbt = path_fps / pathlib.Path("./fps_dbt/")
path_dbt_out = path_dbt/ pathlib.Path("output/")

# Record paths for handoff to other scripts
paths = {
    "data": path_data,
    "logs": path_logs,
    "out": path_out,
    "utils": path_utils,
    # "plot": path_plot,
    "tide": path_tide,
    "tide_data": path_tide_data,
    "dbt": path_dbt,
    "dbt_out": path_dbt_out,
}

# Module level constants and references
# std_pressure = 1013.25  # (mbar)
# kts_to_mps = 0.51444444444  # mps per knt


# %% Main
""" Display task data """

if __name__ == "__main__":
    logger.debug("references ready")
    # print(list(path_tide_data.glob("*.csv")))

# %%
