#!/usr/bin/python3
"""
Defines the `do_deploy` function to distribute an archive to a web server.
"""

import os
from fabric.api import env, put, run
import re

env.hosts = ["54.146.85.222", "52.91.183.35"]


def do_deploy(archive_path):
    """
    Distributes an archive to a web server.
    """
    if not os.path.isfile(archive_path):
        return False

    pattern = r'^(\S+).tgz$'
    match = re.search(pattern, os.path.basename(archive_path))
    if not match:
        return False

    filename = match.group(1)

    if put(archive_path, "/tmp/{}.tgz".format(filename)).failed:
        return False

    commands = [
        "rm -rf /data/web_static/releases/{}/".format(filename),
        "mkdir -p /data/web_static/releases/{}/".format(filename),
        f"tar -xzf /tmp/{filename}.tgz -C /data/web_static/releases/{filename}/",
        "rm /tmp/{}.tgz".format(filename),
        f"mv /data/web_static/releases/{filename}/web_static/* /data/web_static/releases/{filename}/",
        "rm -rf /data/web_static/releases/{}/web_static".format(filename),
        "rm -rf /data/web_static/current",
        f"ln -s /data/web_static/releases/{filename}/ /data/web_static/current"
    ]

    for command in commands:
        if run(command).failed:
            return False

    return True
