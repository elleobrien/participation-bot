import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

token = ""

client = WebClient(token=token)

channel_name = "random"

for result in client.conversations_list():
    channels = result['channels']
    for c in channels:
        if c['name'] == channel_name:
            channel_id = c['id']


# For a given channel id, take a look at what's there
result = client.conversations_history(channel=channel_id, inclusive=True,limit=1)
message=result["messages"]
participants = message[0]['reply_users']


user_id = 'ULELGQWEQ'
result = client.users_info(user=user_id)
