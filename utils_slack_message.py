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
# import sys
import time

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Local Imports


# %% Set up logger
logging.basicConfig(level=logging.DEBUG)
# Verify it works
time_start = time.time()

# %% Functions

def post_message(text):
    """

    """
    assert type(text) is str
    client = WebClient(token=os.environ['slack_bot_token'])
    try:
        response = client.chat_postMessage(channel='C032X2CMSPL', text=text)
        assert response["message"]["text"] == text
    except SlackApiError as err:
        # You will get a SlackApiError if "ok" is False
        assert err.response["ok"] is False
        assert err.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {err.response['error']}")
    return


# %% Main

if __name__ == "__main__":
    text = "hello world!"
    post_message(text)
    print(f"finished in {(time.time() - time_start):.2f}")


# %% Template

# https://api.slack.com/messaging/sending?
# text = "hey world!"
# client = WebClient(token=os.environ['slack_bot_token'])
# try:
#     response = client.chat_postMessage(channel='C032UV1S69G', text=text)
#     assert response["message"]["text"] == text
# except SlackApiError as e:
#     # You will get a SlackApiError if "ok" is False
#     assert e.response["ok"] is False
#     assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
#     print(f"Got an error: {e.response['error']}")
