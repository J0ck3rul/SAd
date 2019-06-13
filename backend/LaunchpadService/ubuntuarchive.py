import gzip
import os
import shutil
import sys
import re
import urllib
from threading import Lock

from constants import PKG_CONTENT_MATCHES
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.abspath('..'))
from PackageClass.package import Package

stdout_lock = Lock()


def get_all_packages():
    existing_archs = ["amd64", "i386"]
    package_list_paths = get_all_package_lists()
    packages = []
    for package_list_path in package_list_paths:
        current_arch = ""
        for arch in existing_archs:
            if arch in package_list_path:
                current_arch = arch
        if not current_arch:
            print "Arch of list {} is unknown.".format(package_list_path)
            return []
        with open(os.path.join("packages", package_list_path), "r") as f:
            package_list_content = f.read()
            for package_info in package_list_content.split("\n\n"):
                if package_info and not package_info.isspace():
                    packages.append(get_pkg_from_list_format(package_info, current_arch))
    return packages


def get_pkg_from_list_format(pkg_info, arch):
    new_pkg_content = {}
    for regex in PKG_CONTENT_MATCHES:
        match = re.search(regex, pkg_info, flags=re.MULTILINE)
        if match:
            if ", " in match.group(1):
                new_pkg_content[PKG_CONTENT_MATCHES[regex]] = [sub_match for sub_match in match.group(1).split(", ")]
            else:
                new_pkg_content[PKG_CONTENT_MATCHES[regex]] = match.group(1)
    if "name" not in new_pkg_content:
        print "Failed to get name"
        return None
    new_pkg_content["architecture"] = arch
    new_pkg = Package(new_pkg_content)
    return new_pkg


def get_all_package_lists():
    downloaded_lists = []
    executor = ThreadPoolExecutor(max_workers=10)
    repo_series = [u'disco', u'cosmic', u'bionic', u'xenial', u'precise', u'trusty']
    repo_series_derivation = ["", "-security", "-updates"]
    repo_type = ["main", "universe", "restricted", "multiverse"]
    repo_arch = ["binary-amd64", "binary-i386"]
    if os.path.exists("packages"):
        shutil.rmtree("packages")
        os.mkdir("packages")
    job_urls = {}
    for series_derivative in repo_series_derivation:
        for series in repo_series:
            dist = series + series_derivative
            for d_type in repo_type:
                for d_arch in repo_arch:
                    archive_filename = "{}_{}_{}_Packages.gz".format(dist, d_type, d_arch)
                    package_list_filename = "{}_{}_{}_packages.list".format(dist, d_type, d_arch)
                    archive_url = "http://archive.ubuntu.com/ubuntu/dists/{}/{}/{}/Packages.gz".format(
                        dist, d_type, d_arch)
                    archive_path = os.path.join("packages", archive_filename)
                    package_list_path = os.path.join("packages", package_list_filename)
                    job_urls[executor.submit(download_package, archive_url, archive_path, package_list_path)] = package_list_filename
    for job in as_completed(job_urls):
        job_filename= job_urls[job]
        try:
            result = job.result()
        except Exception as e:
            stdout_lock.acquire()
            print("Job {} failed with exception: {}".format(job_filename, str(e)))
            stdout_lock.release()
        else:
            stdout_lock.acquire()
            print("Job {} successfully downloaded.".format(job_filename))
            stdout_lock.release()
            downloaded_lists.append(job_filename)
    return downloaded_lists


def download_package(archive_url, archive_path, package_list_path):
    stdout_lock.acquire()
    print "Downloading {}".format(archive_url)
    stdout_lock.release()
    urllib.urlretrieve(archive_url, archive_path)
    with gzip.open(archive_path, "rb") as archive:
        with open(package_list_path, "wb") as package_list:
            archive_content = archive.read()
            package_list.write(archive_content)
    os.remove(archive_path)
    return True
