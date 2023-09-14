from models.point_cloud import PointCloud
from models.testing import launch_main_win


def main():
    pc = PointCloud(mod_fname=Dirs.MODEL_FDIR)
    pc.change_pmesh()
    pc.save_pmesh()
    launch_main_win()


if __name__ == '__main__':
    main()