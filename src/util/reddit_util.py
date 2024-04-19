import datetime
import praw
from praw.models import Subreddit, Submission, Comment

# Initialize PRAW Reddit instance
reddit = praw.Reddit("bot", user_agent="PC:CWRU_CSDS351:v0.1.0 Comment Sentiment Analysis Project (by u/6uep)")


def get_comment_data(comment: Comment) -> dict:
    # See https://praw.readthedocs.io/en/stable/code_overview/models/comment.html for Comment class fields
    return {
        "author": getattr(getattr(comment, "author", ""), "name", ""),
        "body": getattr(comment, "body", ""),
        "upvotes": getattr(comment, "score", 0),
        "comment_date": datetime.datetime.fromtimestamp(getattr(comment, "created_utc", 0)),
        "submission_date": datetime.datetime.fromtimestamp(getattr(getattr(comment, "submission", 0), "created_utc", 0)),
        "comment_id": getattr(comment, "id", ""),
        "submission_id": getattr(getattr(comment, "submission", ""), "id", ""),
        "submission_title": getattr(getattr(comment, "submission", ""), "title", ""),
        "subreddit_id": getattr(getattr(getattr(comment, "submission", ""), "subreddit", ""), "id", ""),
        "subreddit_title": getattr(getattr(getattr(comment, "submission", ""), "subreddit", ""), "display_name", "")
    }


def get_submission_comments(submission: Submission) -> list[Comment]:
    while True:
        try: # replace_more() will return None once there are no more comments to retrieve
            if not submission.comments.replace_more():
                break
        except Exception as e:
            print(e)

    return list(get_comment_data(x) for x in submission.comments)


def get_popular(limit: int = None) -> list[Subreddit]:
    return list(reddit.subreddits.popular(limit=limit))

def get_subreddit(subreddit: str):
    return list(reddit.subreddits.search_by_name(subreddit))

def get_default(limit: int = None) -> list[Subreddit]:
    return list(reddit.subreddits.default(limit=limit))

def get_subreddit_top(name: str, limit: int = None, time_filter: str = "all") -> list[Submission]:
    subreddit: Subreddit = name if isinstance(name, Subreddit) else reddit.subreddit(name)
    return list(subreddit.top(limit=limit, time_filter=time_filter))

def get_subreddit_hot(name: str, limit: int = None) -> list[Submission]:
    subreddit: Subreddit = name if isinstance(name, Subreddit) else reddit.subreddit(name)
    return list(subreddit.hot(limit=limit))

def get_subreddit_new(name: str, limit: int = None) -> list[Submission]:
    subreddit: Subreddit = name if isinstance(name, Subreddit) else reddit.subreddit(name)
    return list(subreddit.new(limit=limit))

def get_subreddit_controversial(name: str, limit: int = None) -> list[Submission]:
    subreddit: Subreddit = name if isinstance(name, Subreddit) else reddit.subreddit(name)
    return list(subreddit.controversial(limit=limit))

def get_subreddit_rising(name: str, limit: int = None) -> list[Submission]:
    subreddit: Subreddit = name if isinstance(name, Subreddit) else reddit.subreddit(name)
    return list(subreddit.rising(limit=limit))
