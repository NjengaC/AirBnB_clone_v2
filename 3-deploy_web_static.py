#!/usr/bin/python3
"""
This script generates a .tgz archive from the web_static folder
and distributes it to web servers using Fabric.
"""


from fabric.api import *
from fabric.api import runs_once
from fabric.api import env
from fabric.api import local
from os.path import exists
from datetime import datetime

env.hosts = ["54.144.140.209", "34.202.233.3"]
env.user = "ubuntu"


def do_pack():
    """
    Generates a .tgz archive from the web_static folder.

    Returns:
        str: Archive path if archive has been generated, otherwise None.
    """
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")

    archive_name = "web_static_{}.tgz".format(current_time)

    archive_path = "versions/{}".format(archive_name)

    print("Packing web_static to {}".format(archive_path))

    local("mkdir -p versions")

    result = local("tar -cvzf {} web_static".format(archive_path))

    if result.succeeded:
        print("web_static packed: {} ".format(archive_path))
        return archive_path
    else:
        print("Failed to pack web_static")
        return None


def do_deploy(archive_path):
    """ Distributes an archive to webserver """

    if not exists(archive_path):
        return False

    print("Deploying new version")

    archive_name = archive_path.split("/")[-1]
    folder_name = archive_name[: -4]
    dir_path = "/data/web_static/releases/{}".format(folder_name)

    put(archive_path, "/tmp/")
    run("mkdir -p {}".format(dir_path))
    result = run("tar -xzf /tmp/{} -C {}".format(archive_name, dir_path))

    if result.failed:
        return False

    run("cp -r {}/web_static/* {}".format(dir_path, dir_path))
    run("rm -rf /tmp/{} {}/web_static".format(archive_name, dir_path))
    run("rm -rf /data/web_static/current")
    run("ln -s {} /data/web_static/current".format(dir_path))

    print("New version deployed!")

    return True


def deploy():
    """
    Main deployment function.
    Creates and deploys a new version locally.
    """
    local_archive_path = do_pack()
    if not local_archive_path:
        print("Failed to create archive.")
        return False

    print("Local archive created successfully : {}".format(local_archive_path))

    extract_path = "/tmp/"
    local("mkdir -p {}".format(extract_path))
    local("tar -xzf {} -C {}".format(local_archive_path, extract_path))

    local("rm -rf /data/web_static/current")
    local("ln -s {}/web_static /data/web_static/current".format(extract_path))

    print("Deployment successful!")
    return True


deploy()
