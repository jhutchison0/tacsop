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


# %% Functions
""" Define functions """


# %% Variables
""" Set script (global) variables """

name_top_package = "GitHub"
name_sub_package = "scrape_wod_daily"

# Local paths
# modify path to utils and data based off cwd (run as utils or fps_server)
if pathlib.Path.cwd().stem == name_sub_package:
    path_local = pathlib.Path.cwd()

elif pathlib.Path.cwd().stem == name_top_package:
    path_local = pathlib.Path(f"{name_sub_package}/")

elif pathlib.Path.cwd().stem == "utils":
    path_local = pathlib.Path("../")

path_data = path_local / pathlib.Path("data/")
path_out = path_local / pathlib.Path("output/")
path_logs = path_local / pathlib.Path("logs/")
path_utils = path_local / pathlib.Path("utils/")

# Ensure cross-package access by modifying path
if ".." not in sys.path:
    sys.path.insert(0, "..")

# External paths
path_top = path_local.parent
path_projects = path_top.parent
path_webdrivers = path_projects / pathlib.Path("webdrivers/")

# Record paths for handoff to other scripts
paths = {
    "data": path_data,
    "logs": path_logs,
    "out": path_out,
    "top": path_top,
    "utils": path_utils,
    "webdrivers": path_webdrivers,
}

# Module level constants and references
# std_pressure = 1013.25  # (mbar)
# kts_to_mps = 0.51444444444  # mps per knt


# %% Main
""" Display task data """

if __name__ == "__main__":
    print("testing local, find .py files")
    print(list(path_local.glob("*.py")))

# %%
