import sys, os
print os.path.abspath('.')
sys.path.insert(0, os.path.abspath('.'))
from PackageClass import Package

import functions
import functions2

def FindPackages(keyword):
    found_packages_names = list(functions.find_package_source(keyword, "ubuntu"))
    for pkg_name in found_packages_names:
        print "DEP:", functions.get_all_dependencies(pkg_name, "ubuntu")


# FindPackages("apache2")
functions.get_all_series()

print functions.get_distro("ubuntu").series_collection_link
pkg_list = functions.get_package_sources("apache2", "ubuntu", "bionic")
for pkg in pkg_list:
        print pkg.display_name
        print pkg.source_package_name
        print pkg.source_package_version
        print ""
# pkg = functions.get_package_binaries("apache2", "ubuntu", "bionic", "amd64")[0]