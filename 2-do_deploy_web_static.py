#!/usr/bin/python3
"""Make .tgz archive from web_static folder and deploy web servers"""

import os
import re
from fabric.operations import local, run, put
from datetime import datetime
from fabric.api import env

env.hosts = ["54.146.85.222", "52.91.183.35"]


def do_pack():
    """Create a .tgz archive"""
    local("mkdir -p versions")
    archive_name = "web_static_{}.tgz".format(
        datetime.strftime(datetime.now(), "%Y%m%d%H%M%S"))
    result = local(
        "tar -cvzf versions/{} web_static".format(archive_name), capture=True)
    if result.failed:
        return None
    return result


def do_deploy(archive_path):
    """Deploy a .tgz archive to a server"""
    if not os.path.exists(archive_path):
        return False
    pattern = r'^versions/(\S+).tgz'
    match = re.search(pattern, archive_path)
    filename = match.group(1)
    result = put(archive_path, "/tmp/{}.tgz".format(filename))
    if result.failed:
        return False
    result = run("mkdir -p /data/web_static/releases/{}/".format(filename))
    if result.failed:
        return False
    result = run(
        "tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/".format(
            filename, filename))
    if result.failed:
        return False
    result = run("rm /tmp/{}.tgz".format(filename))
    if result.failed:
        return False
    result = run(
        "mv /data/web_static/releases/{}/web_static/* "
        "/data/web_static/releases/{}/".format(filename, filename))
    if result.failed:
        return False
    result = run(
        "rm -rf /data/web_static/releases/{}/web_static".format(filename))
    if result.failed:
        return False
    result = run("rm -rf /data/web_static/current")
    if result.failed:
        return False
    result = run(
        "ln -s /data/web_static/releases/{}/ /data/web_static/current".format(
            filename))
    if result.failed:
        return False
    print('New version deployed!')
    return True
