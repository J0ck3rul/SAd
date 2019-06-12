import os
import sys
sys.path.insert(0, os.path.abspath('..'))
from PackageClass.package import Package

import lplib

def FindPackages(keyword):
    found_packages_names = list(lplib.find_package_source(keyword, "ubuntu"))
    for pkg_name in found_packages_names:
        print pkg_name

lplib.find_projects("python")

# print functions.get_all_series()

# print functions.get_distro("ubuntu").series_collection_link
# pkg_list = functions.get_package_sources("apache2", "ubuntu", "bionic")
# for pkg in pkg_list:
#         print pkg.display_name
#         print pkg.source_package_name
#         print pkg.source_package_version
#         print ""
# pkg = functions.get_package_binaries("apache2", "ubuntu", "bionic", "amd64")[0]