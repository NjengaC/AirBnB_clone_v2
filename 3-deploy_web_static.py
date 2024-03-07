#!/usr/bin/python3
""" This script distributes an archive to webservers"""
from fabric.api import local, put, run, env, runs_once
from datetime import datetime
from os.path import isfile


env.hosts = ["54.144.140.209", "34.202.233.3"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"


@runs_once
def do_pack():
    """ Generates a .tgz archive """

    now = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = "web_static_{}.tgz".format(now)
    archive_path = "versions/{}".format(filename)

    print("Packing web_static to {}".format(archive_path))

    local("mkdir -p versions")
    result = local("tar -cvzf {} web_static".format(archive_path))
    if result.failed:
        return None

    print("Successfully packed web_static to {}".format(archive_path))

    return archive_path


def do_deploy(archive_path):
    """ Distributes an archive to webserver """

    if not isfile(archive_path):
        return False

#    print("Deploying new version")

    archive_name = archive_path.split("/")[-1]
    folder_ = archive_name[: -4]
    _path = "/data/web_static/releases/{}".format(folder_)

    put(archive_path, "/tmp/")
    run("mkdir -p {}".format(_path))
    result = run("tar -xzf /tmp/{} -C {}".format(archive_name, _path))

    if result.failed:
        return False

    run("cp -r {}/web_static/* {}".format(_path, _path))
    run("rm -rf /tmp/{} {}/web_static".format(archive_name, _path))
    run("rm -rf /data/web_static/current")
    run("ln -s {} /data/web_static/current".format(_path))

    print("New version deployed!")

    return True


def deploy():
    """ Performs a full deployment from generating archive to deploying """

    filename = do_pack()
    if not filename:
        return False

    return do_deploy(filename)
