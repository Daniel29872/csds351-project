from util.aws_util import *
from util.reddit_util import *

file = open("src/top_subreddits.txt", "r")
subreddits = file.readlines()

print(f"Found {len(subreddits)} subreddits including:", *[f"'{x.title}'" for x in subreddits[:3]])

for subreddit in subreddits:
    submissions = get_subreddit_top(subreddit, limit=5, time_filter="week")
    print(f"Found {len(submissions)} posts in '{subreddit.title}'")

    for submission in submissions:
        try:
            if fetch_count_by_submission_id(submission.id) <= getattr(submission, "num_comments", 0):
                print(f"Searching '{submission.title}' for comments...")
                comments = get_submission_comments(submission)
                print(f"Found {len(comments)} comments")
                insert_many(comments)
        except Exception as e:
            print(e)
