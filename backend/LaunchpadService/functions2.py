import json
import pymongo
from constants import *
from pymongo import MongoClient
from pymongo.errors import BulkWriteError
from launchpadlib.launchpad import Launchpad

launchpad = Launchpad.login_anonymously('just testing', 'production')

client = MongoClient("mongodb://{}:{}@localhost/SAd".format(DB_USERNAME, DB_PASSWORD))
database = client["SAd"]
dist_coll = database[DISTROS_DB]

## Packages ##

def update_db_pkg_list(pkg_list):
    dist_coll.insert_many(pkg_list, ordered=False)


def find_package(pkg_name, online=True):
    if online is False:
        output = list(elem["name"] for elem in dist_coll.find(
            {
                "name": { "$regex": r".*" + pkg_name + r".*" }
            }
        ).sort("name", -1))
        return json.dumps(output, indent=4)
    elif online is True:
        results = []
        for result in launchpad.projects.search(text=pkg_name):
            results.append({"name": result.name})
        update_db_pkg_list(results)
        return find_package(pkg_name, online=False)


def pull_all_packages_into_db():
    project_list = []

    latest_packages = launchpad.projects.latest()
    nr_packages = len(latest_packages)

    total_count = 0
    batch_count = 0

    for project in latest_packages:
        project_list.append({"name": project.name})
        batch_count += 1
        if batch_count == min(nr_packages/100, 100):
            total_count += batch_count
            batch_count = 0
            try:
                update_db_pkg_list(project_list)
            except pymongo.errors.BulkWriteError:
                print "Existing packages found, updating list... [{0:.2g}%]".format((total_count*100)*1.0/nr_packages)
            project_list = []


## Dependencies ##

def get_all_dependencies(pkg_name):
    for pkg in launchpad.archive.search(text=pkg_name):
        return pkg.getArchiveDependency()

## Distros ##

def get_all_distros():
    return list([distro.name for distro in launchpad.distributions])
