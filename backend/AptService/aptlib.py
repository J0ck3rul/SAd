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
    r"^Description[a-zA-Z\-]*: ": "_description",
    r"^Version: ": "_version",
    r"^Depends: ": "_depends",
    r"^Pre-Depends: ": "_pre_depends",
    r"^Conflicts: ": "_conflicts",
    r"^Breaks: ": "_breaks",
    r"^Replaces: ": "_replaces",
    r"^Installed-Size: ": "_installed_size",  # in KB
    r"^Size: ": "_download_size",  # in B
    r"^Homepage: ": "_homepage",
    r"^Maintainer: ": "_maintainer",
    r"^Architecture": "_architecture"

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
    pkg = Package({"name": pkg_name})
    pkg.__dict__
    cmd_output = subprocess.check_output(['apt-cache', "show", pkg_name]).split("\n")
    for attribute in PKG_CONTENT_MATCHES:
        for line in cmd_output:
            match = re.search(attribute, line)
            if match:
                if isinstance(pkg.__dict__[PKG_CONTENT_MATCHES[attribute]], list):
                    arguments = re.sub(attribute, "", line).split(", ")
                else:
                    arguments = re.sub(attribute, "", line)

                pkg.__dict__[PKG_CONTENT_MATCHES[attribute]] = arguments

    return pkg.__dict__


def apt_show_by_version(pkg_name, version):
    pkg = Package({"name": pkg_name})
    pkg.__dict__
    cmd_output = subprocess.check_output(['apt-cache', "show", pkg_name]).split("\n")
    for attribute in PKG_CONTENT_MATCHES:
        for line in cmd_output:
            match = re.search(attribute, line)
            if match:
                if isinstance(pkg.__dict__[PKG_CONTENT_MATCHES[attribute]], list):
                    arguments = re.sub(attribute, "", line).split(", ")
                else:
                    arguments = re.sub(attribute, "", line)

                pkg.__dict__[PKG_CONTENT_MATCHES[attribute]] = arguments

    if version in pkg.__dict__["_version"]:
        return pkg.__dict__
    else:
        return []


def apt_show_by_version_arch(pkg_name, version, arch):
    pkg = Package({"name": pkg_name})
    pkg.__dict__
    cmd_output = subprocess.check_output(['apt-cache', "show", pkg_name]).split("\n")
    for attribute in PKG_CONTENT_MATCHES:
        for line in cmd_output:
            match = re.search(attribute, line)
            if match:
                if isinstance(pkg.__dict__[PKG_CONTENT_MATCHES[attribute]], list):
                    arguments = re.sub(attribute, "", line).split(", ")
                else:
                    arguments = re.sub(attribute, "", line)

                pkg.__dict__[PKG_CONTENT_MATCHES[attribute]] = arguments

    if version in pkg.__dict__["_version"] and arch in pkg.__dict__["_architecture"]:
        return pkg.__dict__
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

print  apt_download("python", "2.7.15~rc1-1", "amd64")
