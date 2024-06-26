#https://dash.plotly.com/tutorial
#https://dash.plotly.com/live-updatess
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
dfGraph['hour'] = dfGraph['submission_date'].dt.hour

# Calculate average score for each hour
hourly_avg_score = dfGraph.groupby('hour')['score'].mean().reset_index()

ALLOWED_TYPES = (
    "text", "number", "password", "email", "search",
    "tel", "url", "range", "hidden",
)

app = Dash(__name__)

app.layout = html.Div(
    html.Div([
        html.Div(children='Subreddit Sentiment Analysis'),
        dcc.Dropdown(subreddits, subreddits[0], id='input-text'),
        dcc.Graph(figure=px.histogram(dfGraph, x='hour', y='score', histfunc='avg'), id='live-update-graph'), #the px.histogram might be slightly wrong?
        dash_table.DataTable(id='live-update-table', data=df[["submission_title", "body", "score"]].to_dict('records'), page_size=10, style_cell={'textAlign': 'left'}),
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
    df = pd.DataFrame(data, columns=["id", "author", "body", "upvotes", "comment_date", "submission_date", "comment_id", "submission_id", "submission_title", "subreddit_id", "subreddit_title", "score"])
    return df[["submission_title", "body", "score"]].to_dict('records')

# v for live updating graph v
# Callback to update the graph
@app.callback(
    Output('live-update-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    # Create a bar plot of hourly average scores
    # Line might be deprecated - plotly.graph_objs.layout.shape.Line
    fig = go.Figure(go.Line(x=hourly_avg_score['hour'], y=hourly_avg_score['score'])) #swap bar to line?
    current_subreddit = df.subreddit_title.unique()[0]
    fig.update_layout(
        title='How is r/' + current_subreddit + ' feeling?',
        xaxis_title='Hour',
        yaxis_title='Average Sentiment',
    )
    return fig

server = app.server

if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8050)

