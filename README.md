# Participation bot

This bot returns a `.csv` summarizing user participation in a channel (# of posts and # of threads replied to per person). 

## Usage
```
$ python bot.py <channel-name> <api-key-file> <from-date> <to-date>
```

For example,
```
$ python bot.py random keys.json 04/08/2021 07/21/2021
```

If the channel is private, you must be a member of the channel and have the proper scope attributed to your API keys.

By default, if no date arguments are given, it takes all messages from April 8th 2021 (date of welcome message in channel) to today's date.

## OAuth Tokens
Slack App OAuth tokens should have `channels:read`, `channels:history`, and `users:read` scope for this script to work on public channels. To work in private channels that you belong to, you'll also need `groups:history` and `groups:read`. 

`bot.py` looks for tokens in a JSON formatted file under the key `"token"`.


