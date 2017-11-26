import dash
from dash.dependencies import Input, Output, Event
import dash_core_components as dcc
import plotly.graph_objs as go
import dash_html_components as html
import datetime
import plotly
import json
import urllib.request
import pandas as pd

app = dash.Dash(__name__)


straight_walk = pd.read_csv('data/axel_walk_fix.csv')[50:200]
left_walk = pd.read_csv('data/axel_halt_fix.csv')[100:250]

app.layout = html.Div(
    html.Div([
        html.H4('Movesense angluar velocity'),
        dcc.Graph(
            figure=go.Figure(
                data=[
                    go.Scatter(
                        x=straight_walk.index,
                        y=straight_walk.foot_1_gyro_z,
                        name='left foot z-velocity',
                        line = dict(
                            color = ('rgb(205, 12, 24)'),
                        )
                    ),
                    go.Scatter(
                        x=straight_walk.index,
                        y=straight_walk.foot_2_gyro_z,
                        name='right foot z-velocity',
                        line = dict(
                            color = ('rgb(42, 85, 170)'),
                        )
                    ),
                ],
                layout=go.Layout(
                    title='Straight walk',
                    showlegend=True,
                    legend=go.Legend(
                        x=0,
                        y=1.0
                    ),
                    margin=go.Margin(l=40, r=0, t=40, b=30)
                )
            ),
            style={
                'height': 250,
            },
            id='straight-walk-graph'
        ),
        dcc.Graph(
            figure=go.Figure(
                data=[
                    go.Scatter(
                        x=left_walk.index,
                        y=left_walk.foot_1_gyro_z,
                        name='left foot z-velocity',
                        line = dict(
                            color = ('rgb(205, 12, 24)'),
                        )
                    ),
                    go.Scatter(
                        x=left_walk.index,
                        y=left_walk.foot_2_gyro_z,
                        name='right foot z-velocity',
                        line = dict(
                            color = ('rgb(42, 85, 170)'),
                        )
                    ),
                ],
                layout=go.Layout(
                    title='Limp walk',
                    showlegend=True,
                    legend=go.Legend(
                        x=0,
                        y=1.0
                    ),
                    margin=go.Margin(l=40, r=0, t=40, b=30)
                )
            ),
            style={
                'height': 250,
            },
            id='left-walk-graph'
        ),
        html.Div(id='live-update-text'),
        html.Div(
            children=[
                html.Div(
                    children=[
                        dcc.Graph(
                                id='live-update-graph',
                                style={
                                    'height': 250,
                                }
                            ),
                        dcc.Interval(
                            id='interval-component',
                            interval=200 # in milliseconds
                        )
                    ],
                ),
                html.Div(
                    children=[
                        html.H4('PLACEHOLDER'),
                        html.H4('Predictions')
                    ],
                ),     
            ])
    ])
)
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

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

    fig = go.Figure(
                data=[
                    go.Scatter(
                        x=data['time'],
                        y=data['x'],
                        name='x-velocity',
                    ),
                    go.Scatter(
                        x=data['time'],
                        y=data['y'],
                        name='y-velocity',
                    ),
                    go.Scatter(
                        x=data['time'],
                        y=data['z'],
                        name='z-velocity',
                    ),
                ],
                layout=go.Layout(
                    title='',
                    showlegend=True,
                    legend=go.Legend(
                        x=0,
                        y=1.0
                    ),
                    margin=go.Margin(l=40, r=0, t=40, b=30)
                )
            )

    return fig


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)
