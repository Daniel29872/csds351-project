import praw

reddit = praw.Reddit("bot", user_agent="bot user agent (by u/6uep)")

print(reddit.user.me())