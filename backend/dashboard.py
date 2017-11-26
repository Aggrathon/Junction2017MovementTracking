# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import peakutils
import pandas as pd

app = dash.Dash()


df = pd.read_csv('data/data.csv')
x_peaks = peakutils.indexes(df.x.values, thres=0.02/max(df.x.values), min_dist=10)
y_peaks = peakutils.indexes(df.y.values, thres=0.02/max(df.y.values), min_dist=10)
z_peaks = peakutils.indexes(df.z.values, thres=0.02/max(df.z.values), min_dist=10)


app.layout = html.Div(children=[
    html.H1(
        children='Angular velocity',
        style={
            'textAlign': 'center',
        }
    ),
    html.Div(children='', style={
        'textAlign': 'center',
    }),
    dcc.Graph(
        figure=go.Figure(
            data=[
                go.Scatter(
                    x=df.index,
                    y=df.x,
                    name='x-acceleration',
                ),
                go.Scatter(
                    x=df.index,
                    y=df.y,
                    name='y-acceleration',
                ),
                go.Scatter(
                    x=df.index,
                    y=df.z,
                    name='z-acceleration',
                ),
                go.Scatter(
                    x=x_peaks,
                    y=df.x.values[x_peaks],
                    mode='markers',
                    name='peaks',
                    line=dict(
                        color='red',
                    )
                ),
                go.Scatter(
                    x=y_peaks,
                    y=df.y.values[y_peaks],
                    mode='markers',
                    name='',
                    line=dict(
                        color='red',
                    )
                ),
                go.Scatter(
                    x=z_peaks,
                    y=df.z.values[z_peaks],
                    mode='markers',
                    name='',
                    line=dict(
                        color='red',
                    )
                )
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
        ),
        style={'height': 600},
        id='my-graph'
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)