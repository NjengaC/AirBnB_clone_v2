#!/usr/bin/python3

"""

"""

import os
from fabric.api import *
from datetime import datetime
from dada import do_deploy
from papa import do_pack

env.hosts = ['54.144.140.209', '34.202.233.3']
env.user = "ubuntu"


def deploy():
    """
    Create and archive and get its path
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
