from models.point_cloud import PointCloud
import gui


def main():
    pc = PointCloud(mod_fname=Dirs.MODEL_FDIR)
    pc.change_pmesh()
    pc.save_pmesh()

    # Docker supports 3.6.11 <= and meshlib requires >= 3.8
    gui.start()


if __name__ == '__main__':
    main()