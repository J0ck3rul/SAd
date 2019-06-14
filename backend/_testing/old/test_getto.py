import re
import getto

# print getto.get_all_distros()
# getto.pull_all_packages_into_db()

def get_installer_package(pkg_name, distro_name, series_name, distro_arch):
    results = getto.get_package_sources(pkg_name, distro_name, series_name)
    if results:
        source_pkg = results[0]
        for deb in source_pkg.binaryFileUrls():
            base_version = re.sub("^[0-9]+:", "", source_pkg.source_package_version)
            if "{}_{}_{}".format(source_pkg.source_package_name, base_version, distro_arch) in deb:
                return deb
            # if "{}_".format(source_pkg.source_package_name) in deb:
            #     print "{}\n{}_{}\n\n".format(deb,source_pkg.source_package_name,base_version)
    return None
    print "Package not found, here are some similar packages:"
    similar_package_sources = getto.find_package_source(pkg_name, distro_name)
    if similar_package_sources:
        for package_source in similar_package_sources:
            print package_source
        return ""
    print "Similar packages not found, here are some similar projects:"
    similar_projects = getto.find_project(pkg_name)
    if similar_projects:
        for project in similar_projects:
            print project
        return ""

# print getto.find_package_source("samba", "ubuntu")
with open("testfile.txt", "r") as f:
    missing_count = 0
    package_list = f.read().split('\n\n')
    for pkg in package_list:
        for pkg_prop in pkg.split('\n'):
            if re.search(r"Package: ", pkg_prop):
                pkg_name = re.sub(r"Package: ", "", pkg_prop)
                if None is get_installer_package(pkg_name, "ubuntu", "bionic", "amd64"):
                    print pkg_name + " not found."
                    missing_count += 1
    print "Missing {} packages, total {}.".format(missing_count, len(package_list))
# print get_installer_package("erlang-guestfs", "ubuntu", "bionic", "amd64")

#IMPORTANT
#chdist for getting packages from other distros

import os
import gzip
import urllib
distros = ["bionic", "bionic-security", "bionic-updates"]
distro_type = ["main", "universe", "restricted", "multiverse"]
distro_arch = ["binary-amd64", "binary-i386"]
os.mkdir("packages")
for dist in distros:
    for d_type in distro_type:
        for d_arch in distro_arch:
            archive_filename = "{}_{}_{}_Packages.gz".format(dist, d_type, d_arch)
            package_list_filename = "{}_{}_{}_packages.list".format(dist, d_type, d_arch)
            print "Downloading http://archive.ubuntu.com/ubuntu/dists/{}/{}/{}/Packages.gz".format(
                dist, d_type, d_arch)
            urllib.urlretrieve("http://archive.ubuntu.com/ubuntu/dists/{}/{}/{}/Packages.gz".format(
                dist, d_type, d_arch),
                os.path.join("packages", archive_filename))
            with gzip.open(os.path.join("packages", archive_filename), "rb") as archive:
                with open(os.path.join("packages", package_list_filename), "wb") as package_list:
                    archive_content = archive.read()
                    package_list.write(archive_content)

