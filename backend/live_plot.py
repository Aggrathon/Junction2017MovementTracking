import dash
from dash.dependencies import Input, Output, Event
import dash_core_components as dcc
import dash_html_components as html
import datetime
import plotly
import json
from flask import Flask, request

flask_app = Flask(__name__)


class LimitedQueue(list):
    def __init__(self, maxlen=100):
        self.maxlen = maxlen + 1

    def append(self, *args): 
        self.extend(args)
        del self[0, len(self) // self.maxlen]

MAX_LIMIT = 1000

data = {
    'time': LimitedQueue(MAX_LIMIT),
    'x': LimitedQueue(MAX_LIMIT),
    'y': LimitedQueue(MAX_LIMIT),
    'z': LimitedQueue(MAX_LIMIT)
}

data['x'].append(1)
data['y'].append(1) 
data['z'].append(1)

@flask_app.route('/', methods=["POST"])
def index():
    # get and parse json data from request body
    content = request.form
    json_data = json.loads(content["test"])
    time = datetime.datetime.now()
    
    if 'ArrayGyro' in json_data['Body']:
        data_type = 'ArrayGyro'
        coords = json_data['Body']['ArrayGyro'][0]

        data['x'].append(float(coords['x']))
        data['y'].append(float(coords['y']))
        data['z'].append(float(coords['z']))
        data['time'].append(time)

    return 'OK', 201

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
    x, y, z = data['x'][-1], data['y'][-1], data['z'][-1]
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
    app.run_server(host='0.0.0.0', debug=True)
    flask_app.run(host='0.0.0.0', debug=True)
