# -*- coding: utf-8 -*-
"""
Created on Tue Feb 07 11:00:00 2023

@author: jhutchison

"""

# %% Packages
""" Third party and local imports """

import pathlib

from datetime import datetime


# %% Functions
""" Define functions """


# %% Variables
""" Set script (global) variables """

path_data = pathlib.Path("data/")
# Specified past date
past_date = datetime(2023, 12, 3, 18)


# %% Main
""" Display task data """

if __name__ == "__main__":
    # Current date
    current_date = datetime.now()

    # Calculate the difference in hours
    time_difference = current_date - past_date
    hours_passed = time_difference.total_seconds() / 3600

    hours_passed
    print(f"{hours_passed} hours since {past_date}")
