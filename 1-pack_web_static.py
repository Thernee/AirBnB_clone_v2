#!/usr/bin/python3
"""Script that makes a tgz archive from the web_static using fabric"""

from os.path import isdir
from datetime import datetime
from fabric.api import local


def do_pack():
    """generates a tgz archive"""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")
        tgz_file = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(tgz_file))
        return tgz_file
    except:
        return None
