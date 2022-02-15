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
import json
import logging
import os
import requests

from bs4 import BeautifulSoup
from datetime import datetime, timedelta

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# %% Date

# Crossfit Daily WOD, record format YYMMDD
today = datetime.today()
tomorrow = today + timedelta(days=1)
# Drop the first two digits of the year
id_tomorrow = tomorrow.strftime(r"%Y%m%d")[2:]

# %% Request today's webpage data


link = "https://www.crossfit.com/workout/"
# Alternative
link = f"https://www.crossfit.com/{id_tomorrow}"
res = requests.get(link)
print(res.status_code == requests.codes.ok)

# %% Request today's webpage data
# res is html

soup = BeautifulSoup(res.text, "lxml")
soup.contents[1]
wod = soup.body.main.article

# wod is a useful markdown text
# there may be a better way to print with formatting

print(wod.get_text())

# %% Set up logger
# logging.basicConfig(level=logging.DEBUG)
# Verify it works

# %% Post to channel
# log handler #1 publish status update
# log handler #2 captures an API error to record locally

client = WebClient(token=os.environ['slack_bot_token'])
response = client.chat_postMessage(channel='C032X2CMSPL', text=f"WOD for today, {id_tomorrow}")
response = client.chat_postMessage(channel='C032X2CMSPL', text=wod.get_text())
# response = client.chat_postMessage(channel='C032X2CMSPL', \

#     blocks={
#         "type": "section",
#         "text": {"type": "mrkdwn", "text": wod.}
#     }
# )

# %% Error
