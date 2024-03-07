#!/usr/bin/python3
""" This script distributes an archive to webservers"""
from fabric.api import local, put, run, env, runs_once
from datetime import datetime
from os.path import isfile


env.hosts = ["54.144.140.209", "34.202.233.3"]
env.user = "ubuntu"


@runs_once
def do_pack():
    """ Generates a .tgz archive """

    now = datetime.now().strftime("%Y%m%d%H%M%S")
    _file = "web_static_{}.tgz".format(now)
    archive_path = "versions/{}".format(_file)

    print("Packing web_static to {}".format(archive_path))

    local("mkdir -p versions")
    local("tar -cvzf {} web_static".format(archive_path))

    print("Successfully packed web_static to {}".format(archive_path))

    return archive_path


def do_deploy(archive_path):
    """ Distributes an archive to webserver """

    if not isfile(archive_path):
        return False

    print("Deploying new version")

    archive = archive_path.split("/")[-1]
    folder_ = archive[: -4]
    _path = "/data/web_static/releases/{}".format(folder_)

    put(archive_path, "/tmp/")
    run("mkdir -p {}".format(_path))
    run("tar -xzf /tmp/{} -C {}".format(archive, _path))
    run("cp -r {}/web_static/* {}".format(_path, _path))
    run("rm -rf /tmp/{} {}/web_static".format(archive, _path))
    run("rm -rf /data/web_static/current")
    run("ln -s {} /data/web_static/current".format(_path))

    print("New version deployed!")

    return True


def deploy():
    """ Performs a full deployment from generating archive to deploying """

    _file = do_pack()
    if not _file:
        return False

    return do_deploy(_file)


@runs_once
def clean_local(number=0):
    """ performs local cleanup """

    versions = local("ls versions", capture=True).split("\n")

    number = int(number)
    if number == 0:
        _keep = 1
    else:
        _keep = number

    _del = versions[: -_keep]
    if len(_del) == 0:
        return

    for i in range(len(_del)):
        _del[i] = "versions/" + _del[i]

    _del = " ".join(_del)

    local("rm {}".format(_del))


def clean_server(number=0):
    """ performs cleanup actions on servers """

    versions = run("ls /data/web_static/releases | grep web_static")
    versions = versions.stdout.split("\n")

    number = int(number)
    if number == 0:
        _keep = 1
    else:
        _keep = number

    _del = versions[: -_keep]
    if len(_del) == 0:
        return

    for i in range(len(_del)):
        _del[i] = _del[i].strip()
        _del[i] = "/data/web_static/releases/" + _del[i]

    _del = " ".join(_del)
    run("sudo rm -rf {}".format(_del))


def do_clean(number=0):
    """ Performs cleanup actions, remove outdated versions, etc """

    clean_local(number)
    clean_server(number)

