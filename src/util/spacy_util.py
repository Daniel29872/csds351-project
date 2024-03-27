import spacy
from aws_util import fetch_posts_from_last_day, update_score
from spacytextblob.spacytextblob import SpacyTextBlob

nlp = spacy.load('en_core_web_sm')
nlp.add_pipe('spacytextblob')

def get_sentiment_polarity(text):
    doc = nlp(text)
    return doc._.blob.polarity

def process_comments_for_sentiment():
    comments = fetch_posts_from_last_day()

    for comment in comments:
        comment_id, comment_body = comment
        sentiment_polarity = get_sentiment_polarity(comment_body)
        update_score(comment_id, sentiment_polarity)

if __name__ == '__main__':
    process_comments_for_sentiment()
