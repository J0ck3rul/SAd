import json
import pymongo
from getto.constants import *
from pymongo import MongoClient
from pymongo.errors import BulkWriteError
from launchpadlib.launchpad import Launchpad

launchpad = Launchpad.login_anonymously('just testing', 'production')

client = MongoClient("mongodb://{}:{}@localhost/SAd".format(DB_USERNAME, DB_PASSWORD))
database = client["SAd"]
dist_coll = database[DISTROS_DB]


def get_all_distros():
    return list([distro.name for distro in launchpad.distributions])


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
                dist_coll.insert_many(project_list, ordered=False)
            except:
                print "Existing packages found, updating list... [{0:.2g}%]".format((total_count*100)*1.0/nr_packages)
            project_list = []