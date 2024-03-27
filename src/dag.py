from util.aws_util import *
from util.reddit_util import *


submissions = get_subreddit_top("politics")
print(f"Found {len(submissions)} posts")

for submission in submissions:
    print(f"Seraching '{submission.title}' for comments...")
    comments = get_submission_comments(submission)
    print(f"Found {len(comments)} comments")
    insert_from_scraper(comments)
