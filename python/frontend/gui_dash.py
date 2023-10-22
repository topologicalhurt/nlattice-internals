from dash import Dash, dcc, html, State, ctx, callback
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from meshlib import mrmeshpy as mm

from python.pc.consts import Conf
from python.frontend.view_model import visualise
from python.lattice_generation.generate_surface_mesh import transform_mesh

# def launch_dash_gui():
app = Dash(__name__)

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

        html.H2("Edge size"),
        dcc.Slider(
            id='edge-size',
            min=0,
            max=10,
            step=0.1,
            value=1
        ),

        html.H2("Tessellation size"),
        dcc.Slider(
            id='tess-size',
            min=0,
            max=10,
            step=0.1,
            value=1
        ),

        html.Button('Convert', id='convert-button', n_clicks=0)
    ], style={'width': '49%', 'display': 'inline-block'}),

    html.Div([
        html.H2("Mesh"),
        dcc.Graph(id='mesh-graph')
    ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
])

@callback(
    Output('mesh-graph', 'figure'),
    [Input('convert-button', 'n_clicks')],
    [State('edge-size', 'value'),
     State('tess-size', 'value'),
     State('tess-option', 'value'),
     State('node-placement-algo-option', 'value')]
)

def update_output(n_clicks, edge_size, tess_size, tess_option, node_placement_algo_option):
    file_path = "./python/lattice_generation/stl_assets/20mm_cube.stl"
    

    if "convert-button" == ctx.triggered_id:
        
        print(edge_size)
        print(tess_size)
        print(tess_option)
        print(node_placement_algo_option)

        # transform_mesh(
        #     path=file_path,
        #     thickness=edge_size,
        #     max_volume_ratio=tess_size,
        #     tesellation_option=tess_option,
        #     node_placement_algo_option=node_placement_algo_option
        # )

        file_path = "./python/lattice_generation/output.stl"
        
        
    mesh = mm.loadMesh(mm.Path(file_path))
    fig = visualise(mesh, edge_size, tess_size)
    return fig

     

app.run_server(debug=True, host='0.0.0.0')