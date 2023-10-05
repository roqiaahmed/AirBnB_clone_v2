#!/usr/bin/python3
"""
Fabric script that Generates a .tgz archive
"""
from fabric.api import *
from datetime import datetime
import os
env.hosts = ['	54.157.165.199', '54.237.14.178']
env.user = 'ubuntu'
def do_pack():
    '''
    Generates a tgz archive from the
    contents of the web_static folder
    '''
    try:
        local('mkdir -p versions')
        time = datetime.now().strftime('%Y%m%d%H%M%S')
        archive_name = 'web_static_{}.tgz'.format(time)
        archive_path = 'versions/{}'.format(archive_name)
        local('tar -czvf {} web_static'.format(archive_path))
        print("web_static packed: {} -> {}Bytes".format(archive_path, os.path.getsize(archive_path)))
    except:
        return None

def do_deploy(archive_path):
    '''
    Deploy archive to web server
    '''
    if not os.path.exists(archive_path):
        return False
    archive_name = archive_path.split("/")[1]
    releases_path = '/data/web_static/releases' + archive_name[:-4]
    try:
        put("{}, /tmp/".format(archive_path))
        run('mkdir -p {}'.format(releases_path))
        run('tar -xvf /tmp/{} -C {}'.format(archive_name, releases_path))
        run('rm -r /tmp/{}'.format(archive_name))
        run('mv {}/web_static/* {}/'.format(releases_path, releases_path))
        run('rm -rf {}/web_static'.format(releases_path))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(releases_path))
        print('New version deployed!')
        return True

    except:
        return False