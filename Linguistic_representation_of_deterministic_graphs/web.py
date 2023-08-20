import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from data import *
from alglib import *
import random


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Br(),
    html.H4('Linguistic representation of D-graph', style={'text-align': 'center'}),
    html.Br(),
    html.I('Root label: ', style={'padding': '10px'}),
    dcc.Input(id='root_data', type='text', value=1, maxLength=1, style={
        'border': '2px solid #ddd',
        'padding': '10px',
        'width': '35px'
    }),
    html.I('C component: ', style={'padding': '10px'}),
    dcc.Input(id='c_data', type='text', placeholder="type C word", style={
        'border': '2px solid #ddd',
        'padding': '10px',
        'width': '300px'
    }),
    html.I('L component: ', style={'padding': '10px'}),
    dcc.Input(id='l_data', type='text', placeholder="type L word", style={
        'border': '2px solid #ddd',
        'padding': '10px',
        'width': '300px'
    }),
    dbc.Button("Submit", id='submit-button', n_clicks=0, color="primary", style={'margin-left': '10px'}),
    html.Br(),
    dcc.Graph(id='network-graph', style={'margin-top': '10px'})
])


@app.callback(
    Output('network-graph', 'figure'),
    Input('submit-button', 'n_clicks'),
    Input('c_data', 'value'),
    Input('l_data', 'value'),
)
def update_graph(n_clicks, c_val, l_val):
    if n_clicks == 0:  # Initial or no button click
        return dash.no_update

    G = ap_graph(tuple(c_val.split()), tuple(l_val.split()))
    # Create Plotly figure from NetworkX graph
    pos = nx.spring_layout(G)  # Layout algorithm (e.g., spring_layout, circular_layout)
    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=1, color='#888'),
        hoverinfo='none',
        mode='lines')

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += (x0, x1, None)
        edge_trace['y'] += (y0, y1, None)

    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            color=[f'rgb({random.randint(100, 255)}, {random.randint(100, 255)}, {random.randint(100, 255)})' for _ in G.nodes()],
            size=25,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            )
        )
    )

    for node in G.nodes():
        x, y = pos[node]
        node_trace['x'] += (x,)
        node_trace['y'] += (y,)
        node_trace['text'] += (f'Node {node}',)

    layout = go.Layout(
        showlegend=False,
        hovermode='closest',
        margin=dict(b=0, l=0, r=0, t=0),
        height=600,
        annotations=[
            dict(
                text=G.nodes[node]['label'],  # Use custom label or default if not found
                x=pos[node][0],
                y=pos[node][1],
                xref='x',
                yref='y',
                showarrow=False,
                font=dict(size=18, color="black")
            )
            for node in G.nodes()
        ]
    )

    fig = go.Figure(data=[edge_trace, node_trace], layout=layout)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
