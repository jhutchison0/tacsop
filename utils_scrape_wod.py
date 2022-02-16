# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 10:58:24 2022

@author: johnk

https://beautiful-soup-4.readthedocs.io/en/latest/

# XML Parser
conda install -c anaconda lxml
"""
# %% Packages

import pandas as pd
# import json
# import logging
import os
import requests

from bs4 import BeautifulSoup
from datetime import datetime, timedelta


# %% Function

def get_wod_cf(date):
    """
    date is a str input YYMMDD
    res is html
    wod is a useful markdown text
    there may be a better way to print with formatting
    """
    assert type(date) is str
    # link = "https://www.crossfit.com/workout/"  # links to all workouts
    link = f"https://www.crossfit.com/{date}"
    res = requests.get(link)
    # print(res.status_code == requests.codes.ok)
    soup = BeautifulSoup(res.text, "lxml")
    soup.contents[1]
    wod = soup.body.main.article
    return wod


def get_wod_c2(date):
    """
    
    """
    link = "https://www.concept2.com/indoor-rowers/training/wod"
    res = requests.get(link)
    print(res.status_code == requests.codes.ok)

    # alternate to "lmxl" is "html.parser"

    soup = BeautifulSoup(res.text, "lxml")
    # wod = soup.find("table", class_="daily-workout-info")
    short = soup.find("section", id="wod-short")
    medium = soup.find("section", id="wod-medium")
    long = soup.find("section", id="wod-long")
    list_wod = [short, medium, long]
    return list_wod


# %% Date

# Crossfit Daily WOD, record format YYMMDD
today = datetime.today()
tomorrow = today + timedelta(days=1)
# Drop the first two digits of the year
id_tomorrow = tomorrow.strftime(r"%Y%m%d")[2:]


# %% Main

if __name__ == "__main__":
    print(get_wod_cf(date=id_tomorrow).get_text())
    print('\n')
    for wod in get_wod_c2(date=id_tomorrow):
        print(wod.get_text())
        print('\n')
