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
print get_installer_package("clif", "ubuntu", "bionic", "amd64")