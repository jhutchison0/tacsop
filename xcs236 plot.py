# -*- coding: utf-8 -*-
"""
Created on Tue Feb 07 11:00:00 2023

@author: jhutchison

"""

# %% Packages
""" Third party and local imports """

import pathlib
import random

# %% Functions
""" Define functions """


# %% Variables
""" Set script (global) variables """

path_data = pathlib.Path("data/")

list_commanders = [
    "abathur",
    "kerrigan",
    "raynor",
    "dehaka",
    "stetman",
    "stukov",
    "mengsk",
    "alarak",
]

# %% Main
""" Display task data """

if __name__ == "__main__":
    rdm_cdr = random.choice(list_commanders)
    print(f"Hello, Commander {rdm_cdr}")
