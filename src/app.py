#In terminal: pip install dash
#run: python <path/to/app.py>
#copy and paste in http link
from dash import Dash, html, dash_table
import pandas as pd

data = pd.read_json("/Users/plschussler/Downloads/environment.json") # replace with "reddit_data.json"

app = Dash(__name__)

app.layout = html.Div([
    html.Div(children='My First App with Data'),
    dash_table.DataTable(data=data.to_dict('records'), page_size=10)
])

if __name__ == '__main__':
    app.run(debug=True)
