import re
import subprocess
from copy import deepcopy

PKG_TEMPLATE = {
    "Name": "",
    "Description": "",
    "Version": "",
    "PreDepends": [],
    "Depends": [],
    "Conflicts": [],
    "Breaks": [],
    "Replaces": []
}

def apt_show(pkg_name):
    pkg = Package(pkg_name)
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

    return pkg

print apt_show("python")