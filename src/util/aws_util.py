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


def insert_many(comments: list[dict]):
    connection, cursor = connect()

    # Only add 1000 or less rows per query
    for i in range(0, len(comments), 1000):
        sql = """INSERT INTO comments (author, body, upvotes, comment_date, submission_date, submission_id, submission_title, subreddit_id, subreddit_title)
                VALUES (%(author)s, %(body)s, %(upvotes)s, %(comment_date)s, %(submission_date)s, %(submission_id)s, %(submission_title)s, %(subreddit_id)s, %(subreddit_title)s)"""
        cursor.executemany(sql, comments[i:i+1000])
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

    sql = """SELECT * FROM comments WHERE score IS NOT NULL ORDER BY score DESC"""
    cursor.execute(sql)
    output = cursor.fetchall()
    connection.close()

    return output


def fetch_count_by_submission_id(id: str):
    connection, cursor = connect()

    sql = """SELECT count(id) FROM comments WHERE submission_id=%s"""
    cursor.execute(sql, (id,))
    output = cursor.fetchall()
    connection.close()
    
    return output[0][0]
