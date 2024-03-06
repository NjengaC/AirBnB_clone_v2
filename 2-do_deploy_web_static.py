#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""

from fabric.api import env, put, run
import os
env.hosts = ["54.144.140.209", "34.202.233.3"]
env.user = 'ubuntu'


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp')

        archive_filename = os.path.basename(archive_path)
        folder_name = '/data/web_static/releases/' + archive_filename[:-4]
        run('sudo mkdir -p {}'.format(folder_name))
        run('sudo tar -xzf /tmp/{} -C {}'
            .format(archive_filename, folder_name))

        # Delete the archive from the web server
        run('sudo rm /tmp/{}'.format(archive_filename))

        # Delete the symbolic link /data/web_static/current from the web server
        run('sudo rm -rf /data/web_static/current')

        run('sudo ln -s {} /data/web_static/current'.format(folder_name))

        print('New version deployed!')
        return True

    except Exception:
        return False
