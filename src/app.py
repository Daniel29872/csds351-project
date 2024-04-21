#https://dash.plotly.com/tutorial
#https://dash.plotly.com/live-updatess
#https://dash.plotly.com/interactive-graphing
#https://dash.plotly.com/dash-core-components/input

#In terminal: pip install dash
#run: python <path/to/app.py>
#copy and paste in http link
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
from util.aws_util import *
import plotly.graph_objs as go
import plotly.express as px
import random

subreddits = fetch_subreddits()

data = fetch_posts_from_subreddit(subreddits[random.randint(0, len(subreddits) - 1)])

df = pd.DataFrame(data, columns=["id", "author", "body", "upvotes", "comment_date", "submission_date", "comment_id", "submission_id", "submission_title", "subreddit_id", "subreddit_title", "score"])

dfGraph = df[['submission_date', 'score']].copy() 

dfGraph['submission_date'] = pd.to_datetime(dfGraph['submission_date'])

# Extract hour from datetime and add it as a new column
dfGraph['date'] = dfGraph['submission_date'].dt.date

# Calculate average score for each day
daily_avg_score = dfGraph.groupby('date')['score'].mean().reset_index()

data_with_scores = fetch_posts_from_last_day_with_score()

dfScores = pd.DataFrame(data_with_scores, columns=["id", "author", "body", "upvotes", "comment_date", "submission_date", "comment_id", "submission_id", "submission_title", "subreddit_id", "subreddit_title", "score"])

dfLeaderboard = dfScores[['subreddit_title', 'score']].copy()

subreddit_avg_score = dfLeaderboard.groupby('subreddit_title')['score'].mean().reset_index()

subreddit_avg_score = subreddit_avg_score.sort_values(by=['score'], ascending=False)

ALLOWED_TYPES = (
    "text", "number", "password", "email", "search",
    "tel", "url", "range", "hidden",
)

app = Dash(__name__)

app.layout = html.Div(
    html.Div([
        html.Div(children='Subreddit Sentiment Analysis'),
        dcc.Dropdown(subreddits, subreddits[0], id='input-text'),
        dcc.Graph(figure=px.histogram(dfGraph, x='date', y='score', histfunc='avg'), id='live-update-graph'), #the px.histogram might be slightly wrong?
        dcc.Markdown('''
## Top 10 most positive comments:'''),
        dash_table.DataTable(id='live-update-table', data=df[["submission_title", "body", "score"]].to_dict('records'), page_size=10, style_cell={'textAlign': 'left','overflow': 'hidden',
        'textOverflow': 'ellipsis',
        'maxWidth': 0}),
        dcc.Markdown('''
## Subreddits ranked by positivity:'''),
        html.Div(
        dash_table.DataTable(id='leaderboard', data=subreddit_avg_score.to_dict('records'), page_size=10, style_cell={'textAlign': 'left','overflow': 'hidden',
        'textOverflow': 'ellipsis',
        'maxWidth': 0})
        ),
        dcc.Interval(
                id='interval-component',
                interval=5*1000, # in milliseconds
                n_intervals=0
        )
    ])
)

@app.callback(
    Output('live-update-table', 'data'),
    Input('interval-component', 'n_intervals'),
    Input("input-text", "value")
)
def update_table(n, text):
    data = fetch_posts_from_subreddit(text)
    df = pd.DataFrame(data, columns=["id", "author", "body", "upvotes", "comment_date", "submission_date", "comment_id", "submission_id", "submission_title", "subreddit_id", "subreddit_title", "score"]).head(10)
    return df[["submission_title", "body", "score"]].to_dict('records')

# v for live updating graph v
# Callback to update the graph
@app.callback(
    Output('live-update-graph', 'figure'),
    Input('interval-component', 'n_intervals'),
    Input("input-text", "value")
)
def update_graph(n, text):
    # Create a bar plot of hourly average scores
    # Line might be deprecated - plotly.graph_objs.layout.shape.Line
    data = fetch_posts_from_subreddit(text)

    df = pd.DataFrame(data, columns=["id", "author", "body", "upvotes", "comment_date", "submission_date", "comment_id", "submission_id", "submission_title", "subreddit_id", "subreddit_title", "score"])

    dfGraph = df[['submission_date', 'score']].copy() 

    dfGraph['submission_date'] = pd.to_datetime(dfGraph['submission_date'])

    # Extract hour from datetime and add it as a new column
    dfGraph['date'] = dfGraph['submission_date'].dt.date

    # Calculate average score for each day
    daily_avg_score = dfGraph.groupby('date')['score'].mean().reset_index()

    fig = go.Figure(go.Line(x=daily_avg_score['date'], y=daily_avg_score['score'])) #swap bar to line?
    
    fig.update_layout(
        title='How is r/' + text + ' feeling?',
        xaxis_title='Day',
        yaxis_title='Average Sentiment',
    )
    return fig

server = app.server

if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8050)

