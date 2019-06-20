import json
import subprocess
import re
import tempfile
from copy import deepcopy
import time
import flask
import io
import os
import sys

from flask import send_file, Flask

sys.path.insert(0, os.path.abspath('..'))
from PackageClass.package import Package

PKG_CONTENT_MATCHES = {
    r"^Package: ": "name",
    r"^Description[a-zA-Z\-]*?: ": "description",
    r"^Architecture: ": "arch",
    r"^Version: ": "version",
    r"^Maintainer: ": "maintainer",
    r"^Installed-Size: ": "installed_size",  # in KB
    r"^Depends: ": "depends",
    r"^Filename: ": "download",
    r"^Size: ": "download_size",  # in B
    r"^Homepage: ": "homepage",
    r"^Pre-Depends: ": "pre_depends",
    r"^Conflicts: ": "conflicts",
    r"^Breaks: ": "breaks",
    r"^Replaces: ": "replaces"
}

# download pkg by name


PKG_TEMPLATE = {
    "Name": "",
    "Description": "",
    "Version": "",
    "PreDepends": [],
    "Depends": [],
    "Conflicts": [],
    "Breaks": [],
    "Replaces": [],
    "Architecture": ""
}


def apt_show(pkg_name):
    pkg = {"name": pkg_name, "pre_depends": [], "depends": [], "conflicts": [], "breaks": [], "replaces": []}
    try:
        cmd_output = subprocess.check_output(['apt-cache', "show", pkg_name]).split("\n")
        for attribute in PKG_CONTENT_MATCHES:
            for line in cmd_output:
                match = re.search(attribute, line)
                if match:
                    if PKG_CONTENT_MATCHES[attribute] not in pkg:
                        pkg[PKG_CONTENT_MATCHES[attribute]] = ""
                    if isinstance(pkg[PKG_CONTENT_MATCHES[attribute]], list):
                        arguments = re.sub(attribute, "", line).split(", ")
                    else:
                        arguments = re.sub(attribute, "", line)
                    pkg[PKG_CONTENT_MATCHES[attribute]] = arguments
        return pkg
    except Exception:
        return []


def apt_show_by_version(pkg_name, version):
    pkg = apt_show(pkg_name)
    if pkg["version"] == version:
        return pkg
    else:
        return []


def apt_show_by_version_arch(pkg_name, version, arch):
    pkg = apt_show_by_version(pkg_name, version)
    if pkg["arch"] == arch:
        return pkg
    else:
        return []


def apt_search_by_name(pkg_name):
    pkg_list = subprocess.check_output(['apt-cache', "search", pkg_name])
    pkg_name_list = []
    for pkg in pkg_list.split("\n"):
        match = re.search(r"^[a-zA-Z0-9\.\-]+", pkg)
        if match:
            pkg_name_list.append(match.group(0))
            # print(match.group(0))
    return pkg_name_list


def apt_download(pkg_name, version, architecture):
    if not apt_show_by_version_arch(pkg_name, version, architecture):
        return "nu exista"
    else:
        temp_dir = tempfile.mkdtemp(prefix="sad")
        subprocess.check_output(["apt-get", "download", pkg_name], cwd=temp_dir)
        file_name = os.listdir(temp_dir)[0]
        file_path = os.path.join(temp_dir, file_name)
        with open(file_path, "rb") as file_handle:
            return file_path


print  apt_show_by_version_arch("python", "2.7.15~rc1-1","amd64")
# print apt_show("pytho")
