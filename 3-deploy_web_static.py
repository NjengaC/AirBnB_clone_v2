#!/usr/bin/python3

"""

"""

import os
from fabric.api import *
from datetime import datetime

env.hosts = ['54.144.140.209', '34.202.233.3']
env.user = "ubuntu"


def do_pack():
    """
    Create a tar gzipped archive of the directory web_static
    """
    now = datetime.now().strftime("%Y%m%d%H%M%S")

    archive_path = "versions/web_static_{}.tgz".format(now)

    local("mkdir -p versions")

    archived = local("tar -cvzf {} web_static".format(archive_path))

    if archived.return_code != 0:
        return None
    else:
        return archive_path


def do_deploy(archive_path):
    """
    use os module to check for valid file path
    """
    if os.path.exists(archive_path):
        archive = archive_path.split('/')[1]
        a_path = "/tmp/{}".format(archive)
        folder = archive.split('.')[0]
        f_path = "/data/web_static/releases/{}/".format(folder)

        put(archive_path, a_path)
        run("sudo mkdir -p {}".format(f_path))
        run("sudo tar -xzf {} -C {}".format(a_path, f_path))
        run("sudo rm {}".format(a_path))
        run("sudo mv -f {}web_static/* {}".format(f_path, f_path))
        run("sudo rm -rf {}web_static".format(f_path))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(f_path))
        return True
    return False


def deploy():
    """
    Create and archive and get its path
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
