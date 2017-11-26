import dash
from dash.dependencies import Input, Output, Event
import dash_core_components as dcc
import dash_html_components as html
import datetime
import plotly
import json
import urllib.request


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
    webURL = urllib.request.urlopen("http://0.0.0.0:5000")
    response_data = webURL.read()
    encoding = webURL.info().get_content_charset('utf-8')
    data = json.loads(response_data.decode(encoding))

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
    webURL = urllib.request.urlopen("http://0.0.0.0:5000")
    response_data = webURL.read()
    encoding = webURL.info().get_content_charset('utf-8')
    data = json.loads(response_data.decode(encoding))

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
