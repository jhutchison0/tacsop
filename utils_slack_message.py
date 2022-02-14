# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 10:58:24 2022

@author: johnk

# run conda from powershell
# conda init --help
conda init cmd.exe
conda init
conda activate base
# pip install slack_sdk
# conda install -c conda-forge slack-sdk
"""
# %% Packages

import logging
import os
import sys

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# %% Set up logger
logging.basicConfig(level=logging.DEBUG)
# Verify it works

# %% Post to channel
# log handler #1 publish status update
# log handler #2 captures an API error to record locally

client = WebClient(token=os.environ['slack_bot_token'])
try:
    response = client.chat_postMessage(channel='C032UV1S69G', text="Hello world!")
    assert response["message"]["text"] == "Hello world!"
except SlackApiError as e:
    # You will get a SlackApiError if "ok" is False
    assert e.response["ok"] is False
    assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
    print(f"Got an error: {e.response['error']}")

# %% Error




