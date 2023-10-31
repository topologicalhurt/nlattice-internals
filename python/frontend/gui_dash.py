from dash import Dash, dcc, html, State, ctx, callback
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from meshlib import mrmeshpy as mm

from python.pc.consts import Conf
from python.frontend.view_model import visualise
from python.lattice_generation.generate_surface_mesh import transform_mesh, tetrahedralize_options
import base64

app = Dash(__name__)
global_path = None


def launch_dash_gui():
    app.run_server(debug=True, host='0.0.0.0')


app.layout = html.Div([
    html.H1("Mesh Visualisation"),

    html.Div([
        html.H2("Tessellation"),
        dcc.RadioItems(
            id='tess-option',
            options=[
                {'label': 'Kagome', 'value': 'Kagome'},
                {'label': 'Tetrahedral', 'value': 'Tetrahedral'},
                {'label': 'Icosahedral', 'value': 'Icosahedral'},
                {'label': 'Voronoi', 'value': 'Voronoi'},
                {'label': 'Rhombic', 'value': 'Rhombic'}
            ],
            value='Kagome'
        ),

        html.H2("Select File"),
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            multiple=False
        ),
        html.Div(id='output-container-button'),


        html.H2("Node placement algorithm"),
        dcc.RadioItems(
            id='node-placement-algo-option',
            options=[
                {'label': 'Delaunay Triangulation', 'value': 'Delaunay Triangulation'},
                {'label': 'Voronoi Triangulation', 'value': 'Voronoi Triangulation'}
            ],
            value='Delaunay Triangulation'
        ),

        html.H2("Triangulation"),
        dcc.RadioItems(
            id='triangulation-option',
            options=[
                {'label': 'Minimum Weight Triangulation', 'value': 'Minimum Weight Triangulation'},
                {'label': 'Bowyer-Watson Triangulation', 'value': 'Bowyer-Watson Triangulation'}
            ],
            value='Minimum Weight Triangulation'
        ),

        html.H2("Wire Thickness"),
        dcc.Slider(
            id='edge-size',
            min=0.1,
            max=1.0,
            step=0.05,
            value=0.1,
            marks={i / 10: str(i / 10) for i in range(0, 11)},
        ),
        html.Div(id='edge-size-label'),

        html.H2("Tesselation Complexity"),
        dcc.Slider(
            id='tess-size',
            min=1.0,
            max=100.0,
            step=1.0,
            value=1.0,
            marks={i * 10: str(i * 10) for i in range(0, 11)},
        ),
        html.Div(id='tess-size-label'),

        html.Button('Convert', id='convert-button', n_clicks=0)
    ], style={'width': '49%', 'display': 'inline-block'}),

    html.Div([
        html.H2("Original Object"),
        dcc.Graph(id='mesh-graph')
    ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
])


@callback(
    [Output('mesh-graph', 'figure'),
     Output('output-container-button', 'children')],
    Input('upload-data', 'filename'))
def update_graph(filename):
    global global_path
    if filename is not None:
        global_path = "python/lattice_generation/stl_assets/" + filename
        try:
            mesh = mm.loadMesh(mm.Path(global_path))
            fig = visualise(mesh, 0.1, 1)
            return fig, 'File found'
        except Exception as e:
            print(e)
            global_path = "python/lattice_generation/stl_assets/20mm_cube.stl"
            mesh = mm.loadMesh(mm.Path(global_path))
            fig = visualise(mesh, 0.1, 1)
            return fig, 'default File loaded'
    else:
        # default filepath
        global_path = "python/lattice_generation/stl_assets/20mm_cube.stl"
        mesh = mm.loadMesh(mm.Path(global_path))
        fig = visualise(mesh, 0.1, 1)
        return fig, 'default File load'


@callback(
    [Output('edge-size-label', 'children'),
     Output('tess-size-label', 'children')],
    [Input('convert-button', 'n_clicks'), Input('edge-size', 'value'), Input('tess-size', 'value')],
    [State('tess-option', 'value'),
     State('node-placement-algo-option', 'value')]
)
def update_output(n_clicks, edge_size, tess_size, tess_option, node_placement_algo_option):
    if "convert-button" == ctx.triggered_id and global_path is not None:
        print(edge_size)
        print(tess_size)
        print(tess_option)
        print(node_placement_algo_option)

        transform_mesh(
            path=global_path,
            thickness=edge_size,
            max_volume_ratio=tess_size,
            tesellation_option=tetrahedralize_options.TETGEN_ADVANCED,
            cell_size=0,
            radius_edge_ratio=0
        )

    return html.Div(f"Current edge size: {edge_size}"), html.Div(f"Current test size: {tess_size}")
