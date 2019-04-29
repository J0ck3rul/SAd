import json
import pymongo
from pymongo import MongoClient
from pymongo.errors import BulkWriteError
from launchpadlib.launchpad import Launchpad

db_username = "devs"
db_password = "devs"

launchpad = Launchpad.login_anonymously('just testing', 'production')

client = MongoClient("mongodb://{}:{}@localhost/tasks_db".format(db_username, db_password))
lp_db = client["lp_db"] # This is the database
lp_coll = lp_db["lp"] # This is a collection (table) in the database

distro = launchpad.distributions["ubuntu"]


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
                lp_coll.insert_many(project_list, ordered=False)
            except:
                print "Existing packages found, updating list... [{0:.2g}%]".format((total_count*100)*1.0/nr_packages)
            project_list = []

def update_db_pkg_list(pkg_list):
    try:
        lp_coll.insert_many(pkg_list, ordered=False)
    except pymongo.errors.BulkWriteError:
        print "Found duplicates, ignoring them..."

def get_all_packages():
    output = list([elem["name"] for elem in lp_coll.find({})])
    output.sort()
    return json.dumps(output, indent=4)

def find_package(pkg_name, online=True):
    if online is False:
        output = list(elem["name"] for elem in lp_coll.find(
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
        


# source = archive.getPublishedSources(exact_match=True, source_name="python2.7", pocket="Release")[0]
# print source.self_link

# with open("db.json", "wb") as f:
#     for pkg in archive.getPublishedSources(pocket="Release"):
#         print pkg
#         json.dump(pkg, f, indent=4)


#for project in launchpad.projects.search(text="python"):
#	if project.name == "python":
#		print project.name


#python27_archive = distro.getArchive(name="python2.7")
#print python27_archive


# archive_obj = json.loads(browser.get(source.self_link))
# print json.dumps(archive_obj, indent=2)


# series = distro.current_series.getDistroArchSeries(archtag="amd64")
# for source in archive.getPublishedBinaries(exact_match=True, binary_name="python2.7", distro_arch_series=series):
#     archive_obj = json.loads(browser.get(source.self_link))
#     print json.dumps(archive_obj, indent=2)
#     print "Archive ID: {}".format(archive_obj["reference"])


#print(launchpad.archive.getByReference
