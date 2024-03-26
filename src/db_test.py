import aws_util
from datetime import datetime

comment = [{"author": "paul attreides", "body": "i am paul muaudib attreides, duke of arrakis", "comment_date": datetime.now(), "upvotes": 2}]

aws_util.insert_from_scraper(comment)
print(aws_util.fetch_posts_from_last_day())

