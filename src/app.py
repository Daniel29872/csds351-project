#https://dash.plotly.com/tutorial
#https://dash.plotly.com/live-updatess

#In terminal: pip install dash
#run: python <path/to/app.py>
#copy and paste in http link
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
from util.aws_util import *
import plotly.graph_objs as go
import plotly.express as px

data = fetch_posts_from_last_day_with_score()
df = pd.DataFrame(data, columns=["id", "author", "body", "upvotes", "comment_date", "submission_date", "comment_id", "submission_id", "submission_title", "subreddit_id", "subreddit_title", "score"])

dfGraph = df[['submission_date', 'score']].copy() 

dfGraph['submission_date'] = pd.to_datetime(dfGraph['submission_date'])

# Extract hour from datetime and add it as a new column
dfGraph['hour'] = dfGraph['submission_date'].dt.hour

# Calculate average score for each hour
hourly_avg_score = dfGraph.groupby('hour')['score'].mean().reset_index()

app = Dash(__name__)

app.layout = html.Div(
    html.Div([
        html.Div(children='Subreddit Sentiment Analysis'),
        #dash_table.DataTable(id='live-update-table', data=df.to_dict('records'), page_size=10),
        dcc.Graph(figure=px.histogram(dfGraph, x='hour', y='score', histfunc='avg'), id='live-update-graph'), #the px.histogram might be slightly wrong?
        dcc.Interval(
                id='interval-component',
                interval=1*1000, # in milliseconds
                n_intervals=0
        )
    ])
)
'''
@app.callback(
    Output('live-update-table', 'data'),
    [Input('interval-component', 'n_intervals')]
)
def update_table(n):
    data = fetch_posts_from_last_day_with_score()
    df = pd.DataFrame(data, columns=["id", "author", "body", "upvotes", "comment_date", "submission_date", "comment_id", "submission_id", "submission_title", "subreddit_id", "subreddit_title", "score"])
    return df.to_dict('records')
'''
# v for live updating graph v
# Callback to update the graph
@app.callback(
    Output('live-update-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    # Create a bar plot of hourly average scores
    fig = go.Figure(go.Line(x=hourly_avg_score['hour'], y=hourly_avg_score['score'])) #swap bar to line?
    fig.update_layout(
        title='How is r/politics feeling?',
        xaxis_title='Hour',
        yaxis_title='Average Sentiment',
    )
    return fig

server = app.server

if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=80)
