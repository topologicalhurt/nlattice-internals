import gui
import subprocess
from models.point_cloud import PointCloud


def main():
    pc = PointCloud(mod_fname=Dirs.MODEL_FDIR)
    pc.change_pmesh()
    pc.save_pmesh()
    gui.start()


if __name__ == '__main__':
    main()