#!/usr/bin/python3
"""
    Fabric script that distributes an archive to my web servers
"""
from fabric.api import *
from fabric.operations import run, put, sudo
import os

env.hosts = ['54.144.140.209', '34.202.233.3']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """
        using fabric to distribute archive
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
        run("sudo tar -xzf /tmp/{} -C {}/{}/"
            .format(new_archive, path, folder[0]))
        run("sudo rm /tmp/{}".format(archive))
        if not run("test -e {}/{}/".format(path, folder[0]),
                   quiet=True).succeeded:
            run("sudo mv -f {}/{}/web_static/* {}/{}/"
                .format(path, folder[0], path, folder[0]))
        run("sudo rm -rf {}/{}/web_static".format(path, folder[0]))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -sf {}/{} /data/web_static/current"
            .format(path, folder[0]))
        return True
    except Exception:
        return False
