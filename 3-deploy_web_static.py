#!/usr/bin/python3
""" Fabric script to generate a .tgz archive from web_static """

from fabric.api import *
import os
from datetime import datetime
env.hosts = ["54.144.140.209", "34.202.233.3"]
env.user = "ubuntu"


def do_pack():
    """ Generates a .tgz archive from the contents of the web_static folder """
    local("mkdir -p versions")

    now = datetime.now()
    file_name = "web_static_{}.tgz".format(now.strftime("%Y%m%d%H%M%S"))

    result = local("tar -cvzf versions/{} web_static".format(file_name))

    if result.succeeded:
        return "versions/{}".format(file_name)
    else:
        return None


def do_deploy(archive_path):
    """Distribute archive."""
    if not os.path.exists(archive_path):
        return False

    try:
        archive_filename = os.path.basename(archive_path)
        version_folder = "/data/web_static/releases/{}".format(
                archive_filename[:-4])

        put(archive_path, "/tmp/")

        run("sudo mkdir -p {}".format(version_folder))
        run("sudo tar -xzf /tmp/{} -C {}/".
                format(archive_filename, version_folder))
        run("sudo rm /tmp/{}".format(archive_filename))

        run("sudo mv -f {}/web_static/* {}".
                format(version_folder, version_folder))

        run("sudo rm -rf {}/web_static".format(version_folder))
        run("sudo rm -rf /data/web_static/current")

        run("sudo ln -s {} /data/web_static/current".format(version_folder))

        print("New version deployed!")
        return True

    except Exception:
        return False


def deploy():
    """
    Create and archive and get its path
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
