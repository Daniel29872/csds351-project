#https://dash.plotly.com/tutorial
#https://dash.plotly.com/live-updatess

#In terminal: pip install dash
#run: python <path/to/app.py>
#copy and paste in http link
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
from util.aws_util import *

data = fetch_posts_from_last_day_with_score()
df = pd.DataFrame(data, columns=["id", "author", "body", "upvotes", "comment_date", "submission_date", "comment_id", "submission_id", "submission_title", "subreddit_id", "subreddit_title", "score"])

app = Dash(__name__)

app.layout = html.Div(
    html.Div([
        html.Div(children='My First App with Data'),
        dash_table.DataTable(id='live-update-table', data=df.to_dict('records'), page_size=10),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
                id='interval-component',
                interval=1*1000, # in milliseconds
                n_intervals=0
        )
    ])
)

@app.callback(
    Output('live-update-table', 'data'),
    [Input('interval-component', 'n_intervals')]
)
def update_table(n):
    data = fetch_posts_from_last_day_with_score()
    df = pd.DataFrame(data, columns=["id", "author", "body", "upvotes", "comment_date", "submission_date", "comment_id", "submission_id", "submission_title", "subreddit_id", "subreddit_title", "score"])
    return df.to_dict('records')

# v for live updating graph v
'''
@app.callback(
    Output('live-update-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
# v Fix this below v
def update_graph(n):
    satellite = Orbital('TERRA')
    data = {
        'time': [],
        'Latitude': [],
        'Longitude': [],
        'Altitude': []
    }

    # Collect some data
    for i in range(180):
        time = datetime.datetime.now() - datetime.timedelta(seconds=i * 20)
        lon, lat, alt = satellite.get_lonlatalt(
            time
        )
        data['Longitude'].append(lon)
        data['Latitude'].append(lat)
        data['Altitude'].append(alt)
        data['time'].append(time)

    # Create the graph with subplots
    fig = plotly.tools.make_subplots(rows=2, cols=1, vertical_spacing=0.2)
    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

    fig.append_trace({
        'x': data['time'],
        'y': data['Altitude'],
        'name': 'Altitude',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1, 1)
    fig.append_trace({
        'x': data['Longitude'],
        'y': data['Latitude'],
        'text': data['time'],
        'name': 'Longitude vs Latitude',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 2, 1)

    return fig
'''

if __name__ == '__main__':
    app.run(debug=True)
