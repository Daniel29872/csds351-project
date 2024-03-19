import datetime
import json

import praw
from praw.models import Submission, Comment

reddit = praw.Reddit("bot", user_agent="bot user agent (by u/6uep)")


def get_post_data(submission: Submission) -> list[dict]:
    while True:
        try:
            if not submission.comments.replace_more():
                break
        except Exception as e:
            print(e)

    return [
        {
            "author": comment.author.name if comment.author else "",
            "body": comment.body,
            "created_date": datetime.datetime.fromtimestamp(comment.created_utc),
            "score": comment.score,
            "comment_id": comment.id,
            "submission_id": submission.id,
            "submission_title": submission.title,
            "subreddit_id": submission.subreddit.id,
            "subreddit_title": submission.subreddit.name
        } 
        for comment in submission.comments
    ]
if __name__ == "__main__":
    submission = reddit.submission(url="https://www.reddit.com/r/pics/comments/1bik7l1/an_orangutan_strolls_through_remains_of_a_former/")
    post_data = get_post_data(submission)
    with open("reddit_data.json", "w") as f:
        json.dump(post_data, f)
