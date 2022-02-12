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
import pandas as pd
# import random
# import re
# import roman
# import seaborn as sns
# import sys
# import time

# from tqdm import tqdm

##############################################################################
# %% Functions


def windspeed(r, V_max, r_max):
    r_out = 1200 * 1000  # meters
    b = 0.25
    m = 1.6
    n = 0.9
    # from excel
    V = V_max * ((r_out - r)/(r_out - r_max))**2
    V = V * (r / r_max)**m
    V = V * np.sqrt(((1 - b) * (n + m)) /
                    (n + m * (r / r_max)**(2 * (n + m))) +
                    (b * (b + 2 * m)) /
                    (1 + 2 * m * (r / r_max)**(2 * m + 1)))
    if ((type(r) == int) | (type(r) == float) | (type(r) == np.float64)):
        return V
    else:
        return(pd.Series(data=V, index=r))


def vel_component(V, radial_line_x, radial_line_y, theta_rad, scale):
    # V, Vtot, or Vtt
    v_x = (radial_line_x - np.sign(np.cos(theta_rad)) *
           (scale * V) *
           (1 / np.sqrt(1 + (np.sin(theta_rad) / np.cos(theta_rad))**2)))
    v_y = (radial_line_y + (scale * V) *
           np.sign(np.cos(theta_rad)) *
           (np.sin(theta_rad) / np.cos(theta_rad)) /
           np.sqrt(1 + (np.sin(theta_rad)/np.cos(theta_rad))**2))
    return v_x, v_y

##############################################################################
# %% Variables
