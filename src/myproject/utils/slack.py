"""Slack webhook posting utility."""

import os

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.web import SlackResponse


def post_message(
    text: str,
    channel: str,
    token: str | None = None,
) -> SlackResponse:
    """Post a message to a Slack channel.

    Args:
        text: Message text to send.
        channel: Slack channel ID (e.g., "C032X2CMSPL").
        token: Bot token. Falls back to the ``SLACK_BOT_TOKEN`` env var.

    Returns:
        Slack API response object.

    Raises:
        SlackApiError: If the Slack API returns an error.
        ValueError: If no token is provided or found in the environment.
    """
    token = token or os.environ.get("SLACK_BOT_TOKEN")
    if not token:
        raise ValueError(
            "Slack bot token required. Pass it directly or set SLACK_BOT_TOKEN."
        )

    client = WebClient(token=token)
    return client.chat_postMessage(channel=channel, text=text)
