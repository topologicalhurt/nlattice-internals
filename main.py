import gui
import subprocess
from models.point_cloud import PointCloud


def main():
    pc = PointCloud(mod_fname=Dirs.MODEL_FDIR)
    pc.change_pmesh()
    pc.save_pmesh()
    
    # Docker supports 3.6.11 <= and meshlib requires >= 3.8
    subprocess.run(['python3.11', 'gui.py'])


if __name__ == '__main__':
    main()
