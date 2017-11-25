import dash
from dash.dependencies import Input, Output, Event
import dash_core_components as dcc
import dash_html_components as html
import datetime
import plotly

import random
import pandas as pd


class Dummy(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

    def get_data(self):
        self.x += random.normalvariate(0, 1)
        self.y += random.normalvariate(0, 1)
        self.z += random.normalvariate(0, 1)
        return self.x, self.y, self.z

class Stream(object):
    def __init__(self):
        self.df = pd.read_csv('data/angular_velocity.csv')
        self.index = 0

    def get_data(self):
        x, y, z = self.df.iloc[self.index]
        self.index += 1
        return x, y, z 

class LimitedQueue(list):
    def __init__(self, maxlen=100):
        self.maxlen = maxlen + 1

    def append(self, *args): 
        self.extend(args)
        self.__delslice__(0, len(self) / self.maxlen)

        
dummy = Stream()

MAX_LIMIT = 60

data = {
    'time': LimitedQueue(MAX_LIMIT),
    'x': LimitedQueue(MAX_LIMIT),
    'y': LimitedQueue(MAX_LIMIT),
    'z': LimitedQueue(MAX_LIMIT)
}

app = dash.Dash(__name__)
app.layout = html.Div(
    html.Div([
        html.H4('Movesense angluar velocity'),
        html.Div(id='live-update-text'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=200 # in milliseconds
        )
    ])
)

# The `dcc.Interval` component emits an event called "interval"
# every `interval` number of milliseconds.
# Subscribe to this event with the `events` argument of `app.callback`
@app.callback(Output('live-update-text', 'children'),
              events=[Event('interval-component', 'interval')])
def update_metrics():
    x, y, z = dummy.get_data()
    style = {'padding': '5px', 'fontSize': '16px'}
    return [
        html.Span('x: {0:.2f}'.format(x), style=style),
        html.Span('y: {0:.2f}'.format(y), style=style),
        html.Span('z: {0:0.2f}'.format(z), style=style)
    ]


# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              events=[Event('interval-component', 'interval')])
def update_graph_live():
    # Collect some data

    time = datetime.datetime.now()
    x, y, z = dummy.get_data()

    data['x'].append(x)
    data['y'].append(y)
    data['z'].append(z)
    data['time'].append(time)

    # Create the graph with subplots
    fig = plotly.tools.make_subplots(rows=3, cols=1, vertical_spacing=0.2)
    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

    fig.append_trace({
        'x': data['time'],
        'y': data['x'],
        'name': 'x-velocity',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1, 1)
    fig.append_trace({
        'x': data['time'],
        'y': data['y'],
        'name': 'y-velocity',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 2, 1)
    fig.append_trace({
        'x': data['time'],
        'y': data['z'],
        'name': 'z-velocity',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 3, 1)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)

