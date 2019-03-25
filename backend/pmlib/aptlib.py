import subprocess
import json
import re
from copy import deepcopy
import time
PKG_CONTENT_MATCHES = {
    r"^Description[a-zA-Z\-]*: ": "_description",
    r"^Version: ": "_version",
    r"^Depends: ": "_depends",
    r"^Pre-Depends: ":"_pre-depends",
    r"^Conflicts: ": "_conflicts",
    r"^Breaks: ": "_breaks",
    r"^Replaces: ": "_replaces",
    r"^Installed-Size: ": "_installed_size",    # in KB
    r"^Size: ": "_download_size",               #in B
    r"^Homepage: ": "_homepage",
    r"^Maintainer: ": "_maintainer"
     


}

PKG_TEMPLATE = {
    "Name" : "",
    "Description" :"",
    "Version": "",
    "PreDepends" : [],
    "Depends": [],
    "Conflicts": [],
    "Breaks": [],
    "Replaces":[]
}

def apt_show(pkg_name):
    cmd_output = subprocess.check_output(['apt-cache',"show",pkg_name])
    pkg = deepcopy(PKG_TEMPLATE)
    for line in cmd_output.split("\n"):
        match=re.search(r"^[a-zA-Z\.\-]+",line)
        if match:
            line=re.sub('Description:',"",line)
            print(line)

    

def apt_search(pkg_name):
    pkg_list = subprocess.check_output(['apt-cache',"search",pkg_name])
    pkg_name_list = []
    for pkg in pkg_list.split("\n"):
        match=re.search(r"^[a-zA-Z0-9\.\-]+",pkg)
        if match:
            pkg_name_list.append(match.group(0))
            # print(match.group(0))
    return pkg_name_list

def apt_get_pkg_obj(pkg_name):
    print(pkg_name)
    cmd_output = subprocess.check_output(['apt-cache',"depends",pkg_name])
    pkg = deepcopy(PKG_TEMPLATE)
    for line in cmd_output.split("\n"):
        match=re.search(r"^  [a-zA-Z0-9]+",line)
        if match:
            info_type = re.sub(r"^  ","",match.group(0))
            match = re.search(r"[a-zA-Z0-9\.\-]+$",line)
            if match:
                info_name = match.group(0)
                pkg[info_type].append(info_name)
    return pkg

def test():
    print("Debian i guess")
    
if __name__ == "__main__":
    apt_show("python")