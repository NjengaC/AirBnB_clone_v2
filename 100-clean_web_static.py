#!/usr/bin/python3
""" Function that deploys """
from fabric.api import *
from fabric.operations import run, local
env.hosts = ['54.144.140.209', '34.202.233.3']
env.user = "ubuntu"


def do_clean(number=0):
    """ CLEANS """

    number = int(number)

    if number == 0:
        number = 2
    else:
        number += 1

    local('cd versions ; ls -t | tail -n +{} | xargs rm -rf'.format(number))
    path = '/data/web_static/releases'
    run('cd {} ; ls -t | tail -n +{} | xargs sudo rm -rf'.format(path, number))
