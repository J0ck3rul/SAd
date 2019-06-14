import re
import LaunchpadService.old.lplib

# print getto.get_all_distros()
# getto.pull_all_packages_into_db()

def get_installer_package(pkg_name, distro_name, series_name, distro_arch):
    results = LaunchpadService.old.lplib.get_package_sources(pkg_name, distro_name, series_name)
    if results:
        source_pkg = results[0]
        for deb in source_pkg.binaryFileUrls():
            base_version = re.sub("^[0-9]+:", "", source_pkg.source_package_version)
            if "{}_{}_{}".format(source_pkg.source_package_name, base_version, distro_arch) in deb:
                return deb
            # if "{}_".format(source_pkg.source_package_name) in deb:
            #     print "{}\n{}_{}\n\n".format(deb,source_pkg.source_package_name,base_version)
    return None
    # print "Package not found, here are some similar packages:"
    # similar_package_sources = getto.find_package_source(pkg_name, distro_name)
    # if similar_package_sources:
    #     for package_source in similar_package_sources:
    #         print package_source
    #     return ""
    # print "Similar packages not found, here are some similar projects:"
    # similar_projects = getto.find_project(pkg_name)
    # if similar_projects:
    #     for project in similar_projects:
    #         print project
    #     return ""

# with open("testfile.txt", "r") as f:
#     missing_count = 0
#     package_list = f.read().split('\n\n')
#     for pkg in package_list:
#         for pkg_prop in pkg.split('\n'):
#             if re.search(r"Package: ", pkg_prop):
#                 pkg_name = re.sub(r"Package: ", "", pkg_prop)
#                 if None is get_installer_package(pkg_name, "ubuntu", "bionic", "amd64"):
#                     print pkg_name + " not found."
#                     missing_count += 1
#     print "Missing {} packages, total {}.".format(missing_count, len(package_list))

#IMPORTANT
#chdist for getting packages from other distros



