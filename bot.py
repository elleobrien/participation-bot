import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import json
from time import sleep
import pandas as pd
import collections
import sys

def get_client(key_file):
    token = json.load(open(key_file))
    client = WebClient(token=token['token'])
    return(client)

def get_channel_id(channel_name, client):
    for result in client.conversations_list(types="public_channel, private_channel"):
        channels = result['channels']
        for c in channels:
            if c['name'] == channel_name:
                return(c['id'])
                
def get_all_posts_in_channel(channel_name, client, max_pages = 5):
    channel_id = get_channel_id(channel_name, client)
    # Note that this will NOT return the full text of replies to posts.
    all_messages = []
    keep_looking = True
    page = 1
    while keep_looking == True and page < max_pages:
        if page == 1:
           result = client.conversations_history(channel=channel_id,limit=200)
        else:
            result = client.conversations_history(channel=channel_id,limit=200, cursor=result['response_metadata']['next_cursor'])
        all_messages = all_messages + result['messages']
        keep_looking = result['has_more']
        sleep(1)
        page +=1    
    return(all_messages)

def get_users_who_posted(messages,return_freq=False):
    # Accepts list of message instances
    users = []
    for msg in messages:
        users.append(msg['user'])
    if return_freq:
        return_users = collections.Counter(users)
    else:
        return_users = set(users)
    return(return_users)

def get_users_who_replied(messages,return_freq=False):
    # Accepts list of message instances
    users = []
    for msg in messages:
        if "reply_users" in msg.keys():
            users += msg["reply_users"]
    if return_freq:
        return_users = collections.Counter(users)
    else:
        return_users = set(users)
    return(return_users)

def get_all_participants_in_channel(messages, return_freq = False):
    posters = get_users_who_posted(messages,return_freq=return_freq)
    repliers = get_users_who_replied(messages,return_freq=return_freq)
    if return_freq:
        all_participants = repliers + posters
    else:
        all_participants = posters.union(repliers)
    return(all_participants)

def user_id_to_uniqname(user_id_list, client):
    uniqnames = []
    for usr in user_id_list:
        try:
            result = client.users_info(user=usr)
            uniqnames.append(result['user']['name'])
        except:
            uniqnames.append('UNK')
            print("Unable to identify user " + usr)
    return(uniqnames)


def user_counts_to_dataframe(counter,context=None):
    df = pd.DataFrame.from_dict(counter, orient='index').reset_index()
    df = df.rename(columns={'index':'user_id', 0:'count'})
    if context:
        df['context'] = context
    return(df)

def make_post_and_reply_summary(messages):
    # Get summaries of post & reply activities
    poster_df = user_counts_to_dataframe(get_users_who_posted(messages,return_freq=True),context='post')
    reply_df = user_counts_to_dataframe(get_users_who_replied(messages, return_freq=True),context='reply')
    # Now concatenate into one big summary dataframe
    participation_df = pd.concat([poster_df,reply_df])
    participation_df['channel'] = channel_name
    # Get usernames of every participant too
    user_list=participation_df['user_id'].unique()
    uniq_name_list = user_id_to_uniqname(user_list, client)
    name_dict = dict(zip(user_list, uniq_name_list))
    participation_df['uniq_name'] = participation_df['user_id'].map(name_dict)
    return(participation_df)


if __name__ == "__main__":
    # Looks for two arguments: a channel name and an API key file
    channel_name = sys.argv[1]
    key_file = sys.argv[2]
    
    client = get_client(key_file)
    channel_id = get_channel_id(channel_name, client)

    # Get messages in the channel of choice
    messages = get_all_posts_in_channel(channel_name, client)
    participation_df = make_post_and_reply_summary(messages)

    # Write to a .csv file
    participation_df.to_csv("report.csv")

