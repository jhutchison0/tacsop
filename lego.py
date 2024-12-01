# -*- coding: utf-8 -*-
"""
Created on Tue Feb 07 11:00:00 2023

@author: jhutchison

"""

# %% Packages
""" Third party and local imports """

import pathlib
import numpy as np


# %% Functions
""" Define functions """


# %% Variables
""" Set script (global) variables """

path_data = pathlib.Path("data/")


# %% Main
""" Display task data """

if __name__ == "__main__":
    print("logger update here, main complete")
    radius = 1.1
    circumfrence = 2 * np.pi * radius
    print(f"{circumfrence=:.2f}")
    distance = 47
    rotations = distance / circumfrence
    print(f"{rotations=:.2f}")


# %%
