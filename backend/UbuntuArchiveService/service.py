import os
import db
import ubuntuarchive
import apt_pkg


apt_pkg.init_system()


def update_package_db():
    packages = ubuntuarchive.get_all_packages()
    db.update_packages_database(packages)


def filter


def get_latest_version_for_package_name(pkg_name, architecture):
    pkgs = db.get_packages_by_name(pkg_name)
    if pkgs:
        versions = [pkg["version"] for pkg in pkgs]
        sortedDict = sorted(versions, cmp=apt_pkg.version_compare, reverse=True)
        return db.get_package_by_name_version_arch(pkg_name, sortedDict[0], architecture)
    else:
        print "Cannot find package ", pkg_name
        return {"version": "N/A"}


