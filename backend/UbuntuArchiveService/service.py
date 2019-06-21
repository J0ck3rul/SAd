import os
import db
import sys
import ubuntuarchive
import apt_pkg

sys.path.insert(0, os.path.abspath('..'))
from UbuntuArchiveService import constants
from ubuntuarchive import get_all_package_lists, get_all_packages_in_list
from gatewayService.dependencysolver import get_dependency_list_for_packages


apt_pkg.init_system()


def update_package_db():
    pkg_lists = get_all_package_lists()
    for pkg_list in pkg_lists:
        packages = ubuntuarchive.get_all_packages_in_list(pkg_list)
        db.update_packages_database(packages)


def get_latest_version_for_package_name(pkg_name, architecture):
    pkgs = db.get_packages_by_name(pkg_name)
    if pkgs:
        versions = [pkg["version"] for pkg in pkgs]
        sortedDict = sorted(versions, cmp=apt_pkg.version_compare, reverse=True)
        return db.get_package_by_name_version_arch(pkg_name, sortedDict[0], architecture)
    else:
        print "Cannot find package ", pkg_name
        return {"version": "N/A"}


def generate_install_script(package_ids_list):
    conflicts_list = []
    package_list = []
    for pkg_id in package_ids_list:
        pkg_obj = db.get_package_by_id(pkg_id)
        package_list.append(pkg_obj)
    pkgs_to_install_list = get_dependency_list_for_packages(package_list)
    template_downloader = "wget -O {0}_{1}_{2}.deb {3}/package/{0}/{1}/{2}/download >/dev/null 2>&1\n"
    template_pkg_name = "{}_{}_{}.deb"
    template_installer = "echo yes | sudo dpkg -i {} || exit\n"

    file_content = "#!/bin/bash\n\n"
    for pkg in pkgs_to_install_list:
        file_content += str(template_downloader).format(
            pkg["name"], pkg["version"], pkg["architecture"], constants.SERVER_PUBLIC_ADDRESS
        )
    file_content += str(template_installer).format(
        " ".join(
            [str(template_pkg_name).format(
                pkg["name"], pkg["version"], pkg["architecture"]
            ) for pkg in pkgs_to_install_list]
        )
    )
    return file_content

