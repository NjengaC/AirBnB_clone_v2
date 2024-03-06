#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""

from datetime import datetime
from fabric.api import *
import os

env.hosts = ["54.144.140.209", "34.202.233.3"]
env.user = "ubuntu"


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

        run("sudo rm -rf {}/web_static".format(version_folder))
        run("sudo mv -f {}/web_static/* {}".
            format(version_folder, version_folder))
        run("sudo rm -rf {}/web_static".format(version_folder))
        run("sudo rm -rf /data/web_static/current")

        run("sudo ln -s {} /data/web_static/current".format(version_folder))

        print("New version deployed!")
        return True

    except Exception as e:
        return False
