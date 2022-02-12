# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 14:50:41 2020

@author: jhutchison

"""

# %% Packages

# import json
# import logging
# import math
# import matplotlib.pyplot as plt
import numpy as np
# import os
# import pandas as pd
# import random
# import re
# import roman
# import seaborn as sns
# import sys
# import time

# from tqdm import tqdm

##############################################################################
# %% Functions


# https://www.movable-type.co.uk/scripts/latlong.html


def get_bearing(lat1, lon1, lat2, lon2):
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    lam1 = np.radians(lon1)
    lam2 = np.radians(lon2)
    dlam = lam2 - lam1
    y = np.sin(dlam) * np.cos(phi2)
    x = np.cos(phi1) * np.sin(phi2) -\
        np.sin(phi1) * np.cos(phi2) * np.cos(dlam)
    theta_rad = np.arctan2(y, x)
    brng = (theta_rad * 180 / np.pi + 360) % 360
    return brng


def get_distance(lat1, lon1, lat2, lon2):
    R = 6371  # km
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    lam1 = np.radians(lon1)
    lam2 = np.radians(lon2)
    dlam = lam2 - lam1
    dphi = phi2 - phi1
    a = np.sin(dphi/2) * np.sin(dphi/2) + (np.cos(phi1) * np.cos(phi2) *
                                           np.sin(dlam/2) * np.sin(dlam/2))
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    d = R * c  # km
    return d  # km


##############################################################################
# %% Variables
