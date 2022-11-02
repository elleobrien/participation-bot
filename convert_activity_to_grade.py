import pandas as pd

assignment_id = "First Slack Stand-up Reports and Responses"


# Get the student uniqnames
team_df = pd.read_csv("students/fa22_student_team_roster.csv")
team_df["uniq_name"] = team_df["email"].str.replace("@umich.edu","")

# For each group that posted a standup, give everyone in the group credit
standup_post_scores = {el:0 for el in team_df["uniq_name"].values}

slack_activity = pd.read_csv("report.csv")
posts = slack_activity[slack_activity["context"]=="post"]

for poster in posts["uniq_name"].values:
    team_id = team_df[team_df["uniq_name"]==poster]["team"].values
    if len(team_id) > 0:
        teammates = team_df[team_df["team"]==team_id[0]]["uniq_name"].values
        for student in teammates:
            if standup_post_scores[student] <1 : # Don't give more points for multiple posts
                standup_post_scores[student] = standup_post_scores[student] + 1
    else:
        print("Team not found for %s" % poster)

# What about comments?
comment_scores = {el:0 for el in team_df["uniq_name"].values}
comments = slack_activity[slack_activity["context"]=="reply"]
more_than_two_comments = comments[comments["count"] >= 2]

for student in more_than_two_comments["uniq_name"].values:
    if student in comment_scores:
        comment_scores[student] = comment_scores[student] + 1
    else:
        print("Did not find %s in student list." % student)

# Add them up!
total_score = {}
for student in team_df["uniq_name"].values:
    total_score[student] = 5*(comment_scores[student] + standup_post_scores[student])

# Turn it into a dataframe
total_score_df = pd.DataFrame.from_dict(total_score, orient="index",columns=["score"])
total_score_df['uniq_name'] = total_score_df.index
total_score_df["email"] = total_score_df["uniq_name"] + "@umich.edu"
total_score_df.reset_index()

filename = "grades/" + "_".join(assignment_id.split(" ")) + ".csv"
total_score_df.to_csv(filename)
