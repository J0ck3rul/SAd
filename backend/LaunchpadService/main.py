import os
import sys
sys.path.insert(0, os.path.abspath('..'))
from PackageClass.package import Package

import lplib
import debdownloader
import ubuntuarchive

# for pkg in lplib.find_package("python3"):
#     print pkg["name"], pkg["distro"], pkg["series"], "amd64"
#     print debdownloader.get_installer_package(pkg["name"], pkg["distro"], pkg["series"], "amd64")
#     print lplib.get_package_sources(pkg["name"], pkg["distro"], pkg["series"])
print ubuntuarchive.get_all_packages()
# print lplib.get_all_series()

# print functions.get_distro("ubuntu").series_collection_link
# pkg_list = functions.get_package_sources("apache2", "ubuntu", "bionic")
# for pkg in pkg_list:
#         print pkg.display_name
#         print pkg.source_package_name
#         print pkg.source_package_version
#         print ""
# pkg = functions.get_package_binaries("apache2", "ubuntu", "bionic", "amd64")[0]