import streamlit as st
from meshlib import mrmeshpy as mm
from python.pc.consts import Conf
from python.frontend.view_model import visualise


def launch_main_win():
    st.title("Mesh Visualisation")

    # Custom CSS to make all buttons the same size
    st.markdown("""
    <style>
        .stButton>button {
            width: 100%;
            height: 60px;
        }
    </style>
    """, unsafe_allow_html=True)

    # Left column
    left_col, right_col = st.columns([2, 1])  # Adjust the ratio of the columns

    with left_col:
        st.subheader("Tessellation")  # Change to subheader for smaller text
        col_1, col_2 = st.columns([1, 1])  # Create two columns side by side
        with col_1:
            if st.button("Kagome"):
                st.write("Kagome selected")
            if st.button("Tetrahedral"):
                st.write("Tetrahedral selected")
            if st.button("Icosahedral"):
                st.write("Icosahedral selected")
            if st.button("Voronoi"):
                st.write("Voronoi selected")
            if st.button("Rhombic"):
                st.write("Rhombic selected")

        st.subheader("Node placement algorithm")  # Change to subheader for smaller text
        col1, col2 = st.columns([1, 1])  # Create two columns side by side
        with col1:
            if st.button("Delaunay Triangulation"):
                st.write("Delaunay Triangulation selected")
            if st.button("Voronoi Triangulation"):
                st.write("Voronoi Triangulation selected")

        with col2:
            if st.button("Minimum Weight Triangulation"):
                st.write("Minimum Weight Triangulation selected")
            if st.button("Bowyer-Watson Triangulation"):
                st.write("Bowyer-Watson Triangulation selected")

        # Slider for edge size
        edge_size = st.slider("Edge size", min_value=0.0, max_value=10.0, value=1.0)
        # Slider for tessellation size
        tess_size = st.slider("Tessellation size", min_value=0.0, max_value=10.0, value=1.0)
        # Create convert button
        if st.button("Convert"):
            st.write("Converted!")
            # #Load the mesh
            # mesh = mm.loadMesh(mm.Path("pokemonstl/bulbasaur_demo.stl"))
            # #Modify mesh using edge_size and tess_size
            # mesh = mm.modifyMesh(mesh, edge_size)
            # mesh = mm.modifyMesh(mesh, tess_size)
            # #Visualise the mesh
            # fig = visualise(mesh, edge_size, tess_size)
            # with right_col:
            #     st.header("Converted Mesh")
            #     st.plotly_chart(fig)
            # st.write("Converted!")

    # Right column
    with right_col:
        st.header("Mesh")
        mesh = mm.loadMesh(mm.Path(Conf.CONFIG['Objects'][0]['Dir']))
        fig = visualise(mesh, edge_size, tess_size)
        st.plotly_chart(fig)
