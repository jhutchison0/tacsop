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

import os
from slack import WebClient

client = WebClient(token=os.environ["SLACK_API_TOKEN"])
# ID of channel you want to post message to
# right click on channel, open channel details, "about" tab, at bottom
channel_id = "C032UV1S69G"  

try:
    # Call the conversations.list method using the WebClient
    result = client.chat_postMessage(
        channel=channel_id,
        text="Hello world!"
        # You could also use a blocks[] array to send richer content
    )
    # Print result, which includes information about the message (like TS)
    print(result)

except SlackApiError as e:
    print(f"Error: {e}")