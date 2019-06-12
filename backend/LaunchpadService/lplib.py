import json
import difflib
from constants import *
from launchpadlib.launchpad import Launchpad

launchpad = Launchpad.login_anonymously('just testing', 'production')


def get_distro(distro_str):
    return launchpad.distributions[distro_str]


def get_all_series():
    series_list = []
    with open("test.json", "r") as f:
        fl = json.load(f)
        for entry in fl["entries"]:
            series_list.append(entry["name"])
    series_list.remove("ff-series")
    return series_list


def get_archive(distro_str, archive_name="primary"):
    distro = get_distro(distro_str)
    return distro.getArchive(
        name=archive_name
    )


def get_distro_series(distro_str, series_str):
    distro = get_distro(distro_str)
    return distro.getSeries(
        name_or_version=series_str
    )


def get_distro_arch_series(distro_str, series_str, arch_str):
    distro_series = get_distro_series(distro_str, series_str)
    return distro_series.getDistroArchSeries(
        archtag=arch_str
    )


def get_package_binaries(pkg, distro_str, series_str, arch_str):
    distro = get_distro(distro_str)
    archive = get_archive(distro_str)
    distro_arch_series = get_distro_arch_series(distro_str, series_str, arch_str)
    return archive.getPublishedBinaries(
        binary_name=pkg, exact_match=True, status="Published", distro_arch_series=distro_arch_series
    )


def get_package_sources(pkg, distro_str, series_str):
    distro = get_distro(distro_str)
    archive = get_archive(distro_str)
    distro_series = get_distro_series(distro_str, series_str)
    return archive.getPublishedSources(
        source_name=pkg, exact_match=True, status="Published", distro_series=distro_series
    )

# def find_package_source(pkg, distro_str):
#     archive = get_archive(distro_str)
#     pkg_results = list(archive.getPublishedSources(
#         source_name=pkg, exact_match=False, status="Published")
#     )
#     returned_pkgs = []
#     for pkg_result in pkg_results:
#         if pkg in pkg_result.source_package_name:
#             if pkg == pkg_result.source_package_name:
#                 return [pkg_result.source_package_name]
#             returned_pkgs.append(pkg_result.source_package_name)
#     returned_pkgs = list(set(returned_pkgs))
#     return difflib.get_close_matches(pkg, returned_pkgs, 8, 0.5)


def pull_packages(packages, distro_str, series_str):
    for package_set in launchpad.packagesets.getBySeries(distroseries=get_distro_series(distro_str, series_str)):
        # print package_set.name
        package_names_list = list(package_set.getSourcesIncluded())
        for pkg_str in package_names_list:
            if pkg_str not in packages:
                packages[pkg_str] = {
                    "distro": distro_str,
                    "series": series_str
                    }


def get_all_packages():
    all_packages = {}
    for distro in launchpad.distributions:
        if distro and distro.current_series:
            pull_packages(all_packages, distro.name, distro.current_series.name)
    return all_packages


def find_package(pkg):
    # print get_all_packages()
    packages = get_all_packages()
    return [
        packages[found_pkg_name]
        for found_pkg_name in difflib.get_close_matches(
            pkg, [pkg_name for pkg_name in packages],
            8,
            0.5
        )]


for pkg_name in find_package("python3"):
    print get_package_sources(pkg_name, pkg_name["distro"], pkg_name["series"])

# get_all_packages()
# package_list = []
# for package_set in launchpad.packagesets.getBySeries(distroseries=get_distro_series("ubuntu", "xenial")):
#     print package_set.name
#     package_list += list(package_set.getSourcesIncluded())
# count = 0
# for pkg in package_list:
#     if "apache" in pkg:
#         count += 1
# print count
