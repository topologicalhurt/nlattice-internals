from models.testing import launch_main_win


def _start():
    launch_main_win()


def start():
    # Docker supports 3.6.11 <= and meshlib requires >= 3.8
    subprocess.run('')
