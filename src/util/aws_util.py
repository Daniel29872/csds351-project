import pymysql
import os
from dotenv import load_dotenv


def connect():
    load_dotenv()
    connection = pymysql.connect(
        host=os.getenv('HOST'),
        port=3306,
        user='admin',
        password=os.getenv('PASSWORD'),
        database=os.getenv('DATABASE')
    )
    return connection, connection.cursor()


def select_all():
    connection, cursor = connect()

    sql = "SELECT * FROM comments"
    cursor.execute(sql)
    output = cursor.fetchall()

    connection.close()
    return output


# Takes a list of dictionaries and inserts them into project.comments
def insert_from_scraper(comments: list[dict]):
    connection, cursor = connect()
    for comment in comments:
        # Initialize varibles
        author = comment.get("author", None)
        body = comment.get("body", None)
        upvotes = comment.get("upvotes", None)
        comment_date = comment.get("comment_date", None)
        submission_date = comment.get("submission_date", None)
        submission_id = comment.get("submission_id", None)
        submission_title = comment.get("submission_title", None)
        subreddit_id = comment.get("subreddit_id", None)
        subreddit_title = comment.get("subreddit_title", None)
        sql = """INSERT INTO comments (author, body, upvotes, comment_date, submission_date, submission_id, submission_title, subreddit_id, subreddit_title)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (author, body, upvotes, comment_date, submission_date, submission_id, submission_title, subreddit_id, subreddit_title))
        connection.commit()
    connection.close()


def update_score(id, score):
    connection, cursor = connect()

    sql = """UPDATE comments 
            SET score = %s
            WHERE id=%s"""
    cursor.execute(sql, (score, id))
    connection.commit()
    connection.close()


def fetch_posts_from_last_day():
    connection, cursor = connect()

    sql = """SELECT id, body FROM comments WHERE comment_date >= NOW() - INTERVAL 1 DAY AND score IS NULL"""
    cursor.execute(sql)
    output = cursor.fetchall()
    connection.close()

    return output

def fetch_posts_from_last_day_with_score():
    connection, cursor = connect()

    sql = """SELECT id, body FROM comments WHERE comment_date >= NOW() - INTERVAL 1 DAY AND score IS NOT NULL"""
    cursor.execute(sql)
    output = cursor.fetchall()
    connection.close()

    return output
