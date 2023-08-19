import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from data import *
from alglib import *
import random


app = dash.Dash(__name__)

G = ap_graph(testC1, testL1)

app.layout = html.Div([
    dcc.Graph(id='network-graph')
])


@app.callback(
    Output('network-graph', 'figure'),
    Input('network-graph', 'relayoutData')  # This can be replaced with other inputs
)
def update_graph(relayoutData):
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
        node_trace['text'] += (f'Node {G.nodes[node]["label"]}',)

    layout = go.Layout(
        showlegend=False,
        hovermode='closest',
        margin=dict(b=0, l=0, r=0, t=0),
        height=700,
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
