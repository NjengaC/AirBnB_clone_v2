#!/usr/bin/python3
"""
Fabric deletes out-of-date archives, using the function do_clean
"""
from fabric.api import *

env.hosts = ["54.144.140.209", "34.202.233.3"]
env.user = "ubuntu"


def do_clean(number=0):
    """
    deletes out-of-date archives, using the function do_clean:
    """
    number = int(number)

    if number == 0 or number == 1:
        number = 2
    else:
        number += 1
    local('cd versions ; ls -t | tail -n +{} | xargs rm -rf'.format(number))
    path = '/data/web_static/releases'
    run('sudo cd {} ; ls -t | tail -n +{} | xargs rm -rf'.format(path, number))
