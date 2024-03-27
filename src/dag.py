from util.aws_util import *
from util.reddit_util import *


submissions = get_subreddit_hot("politics")
print(f"Found {len(submissions)} posts")

for submission in submissions:
    print(f"Searching '{submission.title}' for comments...")
    if fetch_comments_by_submission_id(submission.id) == 0:
        comments = get_submission_comments(submission)
        print(f"Found {len(comments)} comments")
        insert_many(comments)
