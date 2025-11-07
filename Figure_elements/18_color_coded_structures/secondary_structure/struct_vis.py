import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objs as go

# Load data
df_anti = pd.read_csv('secondary_structure/antiterminated_ZTP.csv')
df_term = pd.read_csv('secondary_structure/terminated_ZTP.csv')
df = pd.read_csv('rna_analysis_results.csv', header=None)
df.columns = ['col1', 'col2', 'col3'] + [f'val_{i}' for i in range(df.shape[1] - 3)]

col1_options = sorted(df['col1'].unique())
col2_options = sorted(df['col2'].unique())
col3_options = sorted(df['col3'].unique())

def create_structure_plot(df_structure, title, color_vector=None):
    marker_colors = color_vector if color_vector is not None else 'black'

    backbone = go.Scatter(
        x=df_structure['x'], y=df_structure['y'],
        mode='markers+lines',
        line=dict(color='black'),
        marker=dict(
            size=14,
            color=marker_colors,
            colorscale='Viridis',
            showscale=bool(color_vector),
            colorbar=dict(title='Value') if color_vector is not None else None
        ),
        showlegend=False
    )

    annotations = [
        dict(
            x=row['x'], y=row['y'],
            text=row['nt'],
            xanchor='center', yanchor='middle',
            showarrow=False,
            font=dict(color='white', size=12, family='monospace', weight='bold')
        )
        for _, row in df_structure.iterrows()
    ]

    layout = go.Layout(
        title=title,
        annotations=annotations,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False, scaleanchor='x', scaleratio=1),
        plot_bgcolor='white',
        margin=dict(l=10, r=10, t=40, b=10),
    )

    return go.Figure(data=[backbone], layout=layout)

# Initialize Dash app
app = dash.Dash(__name__)
app.title = 'ZTP Structure Viewer'

app.layout = html.Div([
    html.H1("ZTP Riboswitch Structures", style={'textAlign': 'center'}),
    html.Div([
        html.Label("Column 1"),
        dcc.Dropdown(id='dropdown-col1', options=[{'label': i, 'value': i} for i in col1_options]),

        html.Label("Column 2"),
        dcc.Dropdown(id='dropdown-col2'),

        html.Label("Column 3"),
        dcc.Dropdown(id='dropdown-col3'),
    ], style={'width': '800px', 'margin': '10px'}),

    html.Br(),
    html.Div([
        dcc.Graph(id='graph-anti', style={'width': '50%', 'display': 'inline-block'}),
        dcc.Graph(id='graph-term', style={'width': '50%', 'display': 'inline-block'}),
    ])
])

@app.callback(
    Output('dropdown-col2', 'options'),
    Input('dropdown-col1', 'value')
)
def update_col2_options(selected_col1):
    if selected_col1 is None:
        return []
    options = sorted(df[df['col1'] == selected_col1]['col2'].unique())
    return [{'label': i, 'value': i} for i in options]

@app.callback(
    Output('dropdown-col3', 'options'),
    Input('dropdown-col1', 'value'),
    Input('dropdown-col2', 'value')
)
def update_col3_options(selected_col1, selected_col2):
    if None in (selected_col1, selected_col2):
        return []
    subset = df[(df['col1'] == selected_col1) & (df['col2'] == selected_col2)]
    return [{'label': i, 'value': i} for i in sorted(subset['col3'].unique())]

@app.callback(
    Output('graph-anti', 'figure'),
    Output('graph-term', 'figure'),
    Input('dropdown-col1', 'value'),
    Input('dropdown-col2', 'value'),
    Input('dropdown-col3', 'value')
)
def update_figures(val1, val2, val3):
    if None in (val1, val2, val3):
        return create_structure_plot(df_anti, "ZTP Antiterminated"), create_structure_plot(df_term, "ZTP Terminated")

    row = df[(df['col1'] == val1) & (df['col2'] == val2) & (df['col3'] == val3)]
    color_vector = row.iloc[0, 3:].astype(float).tolist() if not row.empty else None

    return (
        create_structure_plot(df_anti, "ZTP Antiterminated", color_vector),
        create_structure_plot(df_term, "ZTP Terminated", color_vector)
    )

if __name__ == '__main__':
    app.run(debug=True, port=7550)  # Use a different port