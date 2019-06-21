import atexit
import gzip
import os
import re
import shutil
import tempfile
import urllib
from threading import Lock

from concurrent.futures import ThreadPoolExecutor, as_completed

from constants import PKG_CONTENT_MATCHES

TEMP_FOLDER = tempfile.mkdtemp(prefix="sad_")
STDOUT_LOCK = Lock()


def cleanup():
    shutil.rmtree(TEMP_FOLDER)


atexit.register(cleanup)


def get_all_packages_in_list(package_list_path):
    existing_archs = ["amd64", "i386"]
    packages = []
    current_arch = ""
    for arch in existing_archs:
        if arch in package_list_path:
            current_arch = arch
    if not current_arch:
        print "Arch of list {} is unknown.".format(package_list_path)
        return []
    with open(os.path.join(TEMP_FOLDER, package_list_path), "r") as f:
        package_list_content = f.read()
        for package_info in package_list_content.split("\n\n"):
            if package_info and not package_info.isspace():
                packages.append(get_pkg_from_list_format(package_info, current_arch))
    return packages


def get_pkg_from_list_format(pkg_info, arch):
    new_pkg_content = {}
    lists = ["pre_depends", "depends", "conflicts", "breaks", "replaces"]
    for regex in PKG_CONTENT_MATCHES:
        match = re.search(regex, pkg_info, flags=re.MULTILINE)
        if match:
            if ", " in match.group(1):
                new_pkg_content[PKG_CONTENT_MATCHES[regex]] = [sub_match for sub_match in match.group(1).split(", ")]
            else:
                if PKG_CONTENT_MATCHES[regex] in lists:
                    new_pkg_content[PKG_CONTENT_MATCHES[regex]] = [match.group(1)]
                else:
                    new_pkg_content[PKG_CONTENT_MATCHES[regex]] = match.group(1)
    if "name" not in new_pkg_content:
        print "Failed to get name"
        return None
    new_pkg_content["architecture"] = arch
    if "download" in new_pkg_content:
        new_pkg_content["download"] = "http://archive.ubuntu.com/ubuntu/{}".format(new_pkg_content["download"])
    return new_pkg_content


def get_all_package_lists():
    downloaded_lists = []
    executor = ThreadPoolExecutor(max_workers=10)
    repo_series = [u'disco', u'cosmic', u'bionic', u'xenial', u'precise', u'trusty']
    repo_series_derivation = ["", "-security", "-updates"]
    repo_type = ["main", "universe", "restricted", "multiverse"]
    repo_arch = ["binary-amd64", "binary-i386"]
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
                    archive_path = os.path.join(TEMP_FOLDER, archive_filename)
                    package_list_path = os.path.join(TEMP_FOLDER, package_list_filename)
                    job_urls[
                        executor.submit(download_package, archive_url, archive_path, package_list_path)
                    ] = package_list_filename
    for job in as_completed(job_urls):
        job_filename = job_urls[job]
        try:
            job.result()
        except Exception as e:
            STDOUT_LOCK.acquire()
            print("Job {} failed with exception: {}".format(job_filename, str(e)))
            STDOUT_LOCK.release()
        else:
            STDOUT_LOCK.acquire()
            print("Job {} successfully downloaded.".format(job_filename))
            STDOUT_LOCK.release()
            downloaded_lists.append(job_filename)
    return downloaded_lists


def download_package(archive_url, archive_path, package_list_path):
    STDOUT_LOCK.acquire()
    print "Downloading {}".format(archive_url)
    STDOUT_LOCK.release()
    urllib.urlretrieve(archive_url, archive_path)
    with gzip.open(archive_path, "rb") as archive:
        with open(package_list_path, "wb") as package_list:
            archive_content = archive.read()
            package_list.write(archive_content)
    os.remove(archive_path)
    return True
