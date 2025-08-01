"""
Preliminary module design, mvp prototype.
"""
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.graph_objs as go
import random
import networkx as nx

from AlgorithmsLibraries.alglib_prod_version_1_0_0 import *
# from AlgorithmsLibraries.alglib_version_02_current import \
#     ap_graph, get_canonical_pair_metrics_from_dgraph, compression


#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

load_figure_template("spacelab")
app = dash.Dash(external_stylesheets=[dbc.themes.SPACELAB])

root_input = html.Div(
    [
        dbc.Label("Root label: ", html_for="root_data"),
        dbc.Input(type="text", id="root_data", value='0', maxLength=1 , style={"width": "36px"}),
        dbc.FormText(
            "root label must be a char: '1' or 'A' etc ... ",
            color="secondary",
        ),
    ],
    className="mb-3",
)

c_input = html.Div(
    [
        dbc.Label("C component: ", html_for="c_data"),
        dbc.Input(type="text", id="c_data", placeholder="Enter words that described graph cycles"),
        dbc.FormText(
            "Input example: 01210 01242154312310 02352510 02130214210 01320213025310 01323510 02141345320 015452034531210 0214130251320 01352101421320",
            color="secondary",
        ),
    ],
    className="mb-3",
)

l_input = html.Div(
    [
        dbc.Label("L component: ", html_for="l_data"),
        dbc.Input(type="text", id="l_data", placeholder="Enter words that described leaf nodes"),
        dbc.FormText(
            "Input example: 0235431302105 012410120314",
            color="secondary",
        ),
    ],
    className="mb-3",
)

fsp_input = html.Div(
    [
        dbc.Label("Word for compress: ", html_for="fsp_data"),
        dbc.Input(type="text", id="fsp_data", placeholder="Enter correct word for finding shortest path to node"),
        dbc.FormText(
            "Input example: 015214215",
            color="secondary",
        ),
    ],
    className="mb-3",
)

submit_btn = html.Div(
    [
        dbc.Button("Make graph", id='submit-button', n_clicks=0, color="primary", style={'marginRight': '10px'}),
        dbc.Button("Compress pair", id='new-action-button', n_clicks=0, color="secondary")
    ]
)

form = dbc.Form([
    dbc.Row([
        dbc.Col(root_input, width=4),
        dbc.Col(fsp_input, width=8),
    ], className="mb-3"),

    dbc.Row([
        dbc.Col(c_input, width=12),
    ], className="mb-3"),

    dbc.Row([
        dbc.Col(l_input, width=12),
    ], className="mb-3"),

    dbc.Row([
        dbc.Col(submit_btn),
    ])
])

app.layout = dbc.Container(
    html.Div([
        html.Br(),
        html.H4('Linguistic Presentation of D-graph', style={'textAlign': 'center'}),
        html.Br(),
        form,
        html.Br(),
        html.Div(id='error-message', style={'color': 'red'}),
        html.Br(),
        html.H4('graph metrics: ', style={'textAlign': 'center'}),
        html.Br(),
        dbc.Textarea(id='output-text', value='', style={'width': '100%', 'height': 100}),
        html.Br(),
        dcc.Graph(id='network-graph', style={'marginTop': '10px', 'marginBottom': '10px'}),
        html.Br(),
        html.Footer(
            html.P("IAMM proceedings 2022 - 2025")
        ),
    ])
)


@app.callback(
    [Output('network-graph', 'figure'),
     Output('output-text', 'value'),
     Output('error-message', 'children')],
    [Input('submit-button', 'n_clicks'),
     Input('new-action-button', 'n_clicks')],
    [State('c_data', 'value'),
     State('l_data', 'value'),
     State('root_data', 'value'),
     State('fsp_data', 'value')]
)
def update_graph_or_new_action(submit_n_clicks, new_action_n_clicks, c_val, l_val, root_val, fsp_val):
    # Определяем, какая кнопка была нажата
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update, '', ''

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Если была нажата кнопка "Submit"
    if triggered_id == 'submit-button':
        try:
            c_component = tuple(c_val.split()) if c_val else tuple()
            l_component = tuple(l_val.split()) if l_val else tuple()
            G = ap_graph(c_component, l_component, root_val)
        except ValueError as e:
            return dash.no_update, '', f'Error: {str(e)} Please check your input.'

        pos = nx.spring_layout(G)
        edge_trace = go.Scatter(
            x=[], y=[], line=dict(width=1, color='#888'), hoverinfo='none', mode='lines'
        )

        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace['x'] += (x0, x1, None)
            edge_trace['y'] += (y0, y1, None)

        node_trace = go.Scatter(
            x=[], y=[], text=[], mode='markers', hoverinfo='text',
            # marker=dict(
            #     showscale=True, colorscale='YlGnBu',
            #     color=[f'rgb({random.randint(100, 255)}, {random.randint(100, 255)}, {random.randint(100, 255)})'
            #            for _ in G.nodes()],
            #     size=35, colorbar=dict(thickness=15, title='Node Connections', xanchor='left', titleside='right')
            # )
            marker=dict(
                showscale=True,
                colorscale='YlGnBu',
                color=[f'rgb({random.randint(100, 255)}, {random.randint(100, 255)}, {random.randint(100, 255)})'
                       for _ in G.nodes()],
                size=35,
                colorbar=dict(
                    thickness=15,
                    xanchor='left',
                    title=dict(
                        text='Node Connections',
                        side='right'
                    )
                )
            )

        )

        for node in G.nodes():
            x, y = pos[node]
            node_trace['x'] += (x,)
            node_trace['y'] += (y,)
            node_trace['text'] += (f'Node {node}',)

        layout = go.Layout(
            showlegend=False, hovermode='closest', margin=dict(b=0, l=0, r=0, t=0), height=600,
            annotations=[
                dict(text=G.nodes[node].get('label', node), x=pos[node][0], y=pos[node][1], xref='x', yref='y',
                     showarrow=False, font=dict(size=18, color="black"))
                for node in G.nodes()
            ]
        )
        fig = go.Figure(data=[edge_trace, node_trace], layout=layout)

        output_text = str(get_canonical_pair_metrics_from_dgraph(G))

        return fig, output_text, ''

    elif triggered_id == 'new-action-button':

        c_component = tuple(c_val.split()) if c_val else tuple()
        l_component = tuple(l_val.split()) if l_val else tuple()
        fsp_word = fsp_val if fsp_val else ""

        if validate_defining_pair(c_component, l_component, root_val):
            compression_data = compression(c_component, l_component)
            fsp_result = find_shortest_path_by_word(fsp_word, list(compression_data['compressed_pair'][0]))
            result = f"{compression(c_component, l_component)} \n Shortest path by word compression: {fsp_result}"
        else:
            return dash.no_update, '', f'Error: Please check your input.'

        return dash.no_update, result, ''

    return dash.no_update, '', ''


if __name__ == '__main__':
    #app.run_server(debug=True)
    app.run(debug=True)