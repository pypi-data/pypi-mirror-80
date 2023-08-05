"""
Various functions shared between the other modules
"""
import socket
import platform
import zipfile
import os
import yaml
from yaml.constructor import ConstructorError


def gethostname():
    try:
        return socket.gethostname()
    except:
        return "unknown-hostname"


def iswindows():
    return platform.system() == "Windows"


def parse_config(configfile):
    with open(configfile, "r") as infile:
        try:
            config = yaml.load(infile, Loader=yaml.SafeLoader)
        except ConstructorError:
            # this file probably has unicode still in it, use the full loader
            config = yaml.load(infile, Loader=yaml.FullLoader)

    assert config

    assert "server" in config
    assert "dir" in config
    assert "executor" in config
    assert "token" in config
    assert "shell" in config

    return config


def save_config(configfile, data):
    with open("gitlab-runner.yml", "w") as outfile:
        yaml.safe_dump(data, outfile, indent=2)


class ZipFileEx(zipfile.ZipFile):
    """
    A variant of ZipFile that restores file permissions where supported
    """
    # inspired mostly from https://stackoverflow.com/a/39296577/148415

    def _extract_member(self, member, targetpath, pwd):
        """
        Extract a member from the zip file and restore permission bits, also ensure that
        the file is readable and writable by the owner
        :param member:
        :param path:
        :param pwd:
        :return:
        """
        if not isinstance(member, zipfile.ZipInfo):
            member = self.getinfo(member)
        ret_val = super(ZipFileEx, self)._extract_member(member, targetpath, pwd)
        if not iswindows():
            attr = member.external_attr >> 16
            os.chmod(ret_val, attr | 0o600)
        return ret_val
