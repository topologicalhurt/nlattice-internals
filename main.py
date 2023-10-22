import argparse
import pymesh as pm
import subprocess

from python.utils.utils import time_it
from python.pc.consts import Dirs
from python.pc.point_cloud import PointCloud
from python.frontend.gui import launch_main_win_streamlit
from python.frontend.gui_dash import launch_dash_gui
# from python.frontend.gui import launch_main_win_streamlit, draw_line_3d

parser = argparse.ArgumentParser(description='Nlattice is a 3D mesh latticing lib. Read more here: ' +
                                             'https://github.com/topologicalhurt/nlattice-internals')
parser.add_argument('--no-gui', action='store_true', help='Flag which determines if GUI is on or off')
parser.add_argument('--cache-pmesh', action='store_true', help='Flag which determines if object is cached in out')
parser.add_argument('--test', action='store_true', help='Flag which determines to display a test intersection')
parser.add_argument('-ui', action='store', choices=['streamlit', 'dash', 'none'], help='Parameter providing the GUI to use (streamlit, dash)')
parser.add_argument('--stwrapper', action='store_true', help='If script is detected as being run by streamlit wrapper call')
args = parser.parse_args()


if __name__ == '__main__':
    if not args.no_gui:
        match args.ui:
            case "streamlit":
                print('launching streamlit wrapper...')
                subprocess.run(['streamlit', 'run', 'main.py', '--', '--stwrapper', '-ui', 'none'])
            case "dash":
                print('launching dash gui...')
                launch_dash_gui()
                # subprocess.run(['python', 'python/frontend/gui_dash.py'])
            case 'none':
                pass
            case _:
                pass


class SharedPc:
    """"Basic PTR pattern - points to the point cloud so main() doesn't have to be encapsulated in a class"""
    def __init__(self):
        self._pc = None

    def set_pc(self, pc: pm.Mesh):
        self._pc = pc

    def get_pc(self):
        return self._pc


@time_it
def main(spc: SharedPc):

    pc = PointCloud(mod_fname=Dirs.MODEL_FDIR)

    if args.test:
        spc.set_pc(pc)
        print('Running benchmark on mesh...')
        pc.intersect_pmesh()
        print('Creating mesh point point cloud...')
        pc.create()

    if args.cache_pmesh:
        print('Caching pmesh...')
        pc.save_pmesh()


if __name__ == '__main__':
    if args.stwrapper:
        shared_pc = SharedPc()
        main(shared_pc)
        point_cloud = shared_pc.get_pc()
        print('running streamlit in wrapper')
        # launch_main_win_streamlit(centroid_coincident=point_cloud.get_centroid_coincident(),
        #                           draw_centroid_coincident=True)
        launch_main_win_streamlit()
