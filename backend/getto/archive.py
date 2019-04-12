import difflib
from getto.constants import *
from launchpadlib.launchpad import Launchpad

launchpad = Launchpad.login_anonymously('just testing', 'production')

def get_distro(distro_str):
    return launchpad.distributions[distro_str]

def get_archive(distro_str):
    distro = get_distro(distro_str)
    return distro.getArchive(name="primary")

def get_distro_series(distro_str, series_str):
    distro = get_distro(distro_str)
    return distro.getSeries(name_or_version=series_str)

def get_distro_arch_series(distro_str, series_str, arch_str):
    distro_series = get_distro_series(distro_str, series_str)
    return distro_series.getDistroArchSeries(archtag=arch_str)

def get_package_binaries(pkg, distro_str, series_str, arch_str):
    distro = get_distro(distro_str)
    archive = get_archive(distro_str)
    distro_arch_series = get_distro_arch_series(distro_str, series_str, arch_str)
    return archive.getPublishedBinaries(binary_name=pkg, exact_match=True, status="Published", distro_arch_series=distro_arch_series)

def get_package_sources(pkg, distro_str, series_str):
    distro = get_distro(distro_str)
    archive = get_archive(distro_str)
    distro_series = get_distro_series(distro_str, series_str)
    return archive.getPublishedSources(source_name=pkg, exact_match=True, status="Published", distro_series=distro_series)

def find_package_source(pkg, distro_str):
    archive = get_archive(distro_str)
    pkg_results = list(archive.getPublishedSources(source_name=pkg, exact_match=False, status="Published"))
    returned_pkgs = []
    for pkg_result in pkg_results:
        if pkg in pkg_result.source_package_name:
            if pkg == pkg_result.source_package_name:
                return [pkg_result.source_package_name]
            returned_pkgs.append(pkg_result.source_package_name)
    returned_pkgs = list(set(returned_pkgs))
    return difflib.get_close_matches(pkg, returned_pkgs, len(returned_pkgs), 0.5)
