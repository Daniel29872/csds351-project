import spacy
import nltk
from aws_util import fetch_posts_from_last_day, update_score
from spacytextblob.spacytextblob import SpacyTextBlob
from nltk.sentiment import SentimentIntensityAnalyzer

nlp = spacy.load('en_core_web_sm')
nltk.download('vader_lexicon')

def get_textblob_sentiment_polarity(text):
    nlp.add_pipe('spacytextblob')
    doc = nlp(text)
    return doc._.blob.polarity

def get_nltk_sentiment_polarity(text):
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(text)['compound']

def get_average_sentiment(text):
    return (get_textblob_sentiment_polarity(text) + get_nltk_sentiment_polarity(text)) / 2

def process_comments_for_sentiment():
    comments = fetch_posts_from_last_day()

    for comment in comments:
        comment_id, comment_body = comment
        sentiment_polarity = get_average_sentiment(comment_body)
        update_score(comment_id, sentiment_polarity)

if __name__ == '__main__':
    process_comments_for_sentiment()
