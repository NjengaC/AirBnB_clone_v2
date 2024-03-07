#!/usr/bin/python3
""" Fabric script to generate a .tgz archive from web_static """

from fabric.api import local
from datetime import datetime
from fabric.api import *
from fabric.operations import run, put, sudo
import os

env.hosts = ['54.144.140.209', '34.202.233.3']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'
archive_path = None


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
    """
    distributes an archive to web servers, using the function do_deploy
    """
    if os.path.isfile(archive_path) is False:
        return False
    try:
        archive = archive_path.split("/")[-1]
        path = "/data/web_static/releases"
        put("{}".format(archive_path), "/tmp/{}".format(archive))
        folder = archive.split(".")
        run("sudo mkdir -p {}/{}/".format(path, folder[0]))
        new_archive = '.'.join(folder)
        run("sudo tar -xzf /tmp/{} -C {}/{}/ --strip-components=1"
            .format(new_archive, path, folder[0]))
        run("sudo rm /tmp/{}".format(archive))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -sf {}/{} /data/web_static/current"
            .format(path, folder[0]))
        print("New version deployed!")
        return True
    except Exception:
        return False


def deploy():
    """
    Create and archive and get its path
    """
    global archive_path
    if archive_path is None:
        archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
