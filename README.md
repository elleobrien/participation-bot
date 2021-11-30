# Participation Bot

## Step 1: Slack Channel Report Generation (bot.py)

This bot returns a `.csv` summarizing user participation in a channel (# of posts and # of threads replied to per person).
This bot requires a keys.json with Slack API keys to access the MADS Slack.

### Generating OAuth Tokens (One Time)
Slack App OAuth tokens should have `channels:read`, `channels:history`, and `users:read` scope for this script to work on public channels. To work in private channels that you belong to, you'll also need `groups:history` and `groups:read`.

`bot.py` looks for tokens in a JSON formatted file under the key `"token"`.

### Usage of bot.py

```
$ python bot.py <channel-name> <api-key-file> <from-date> <to-date>
```

For example,
```
$ python bot.py siads697_fa21_001_standups keys.json 10/30/2021 11/07/2021
```

If the channel is private, you must be a member of the channel and have the proper scope attributed to your API keys.

By default, if no date arguments are given, it takes all messages from the date of welcome message in channel to today's date.

## Step 2: Grading (convert_activity_to_grade.py)

This bot requires an updated student team roster in the students folder.

### Generating Student Roster
To generate the student roster for this course, go to Learners -> Teams and download the Team Roster. Then, reformat the table to assign unique keys to each team and make the CSV 1 row per student (like student_team_dictionary1.csv in students/). Name this csv student_team_dictionary.csv in students/

### Usage of convert_activity_to_grade.py

Update the assignment ID at the top of the Python file to the exact name of the next assignment. i.e.
```
assignment_id = "First Slack Stand-up Reports and Responses"
```

Create a 'grades' folder within 'participation-bot'. Then, create the correct csv file within the grades folder and leave it empty. i.e. ('participation-bot/grades/First_Slack_Stand-up_Reports_and_Responses.csv')

Then run the bot:

```
$ python convert_activity_to_grade.py
```

This generates a final csv with the correct grades!
