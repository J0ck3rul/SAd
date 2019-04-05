import json
from launchpadlib.launchpad import Launchpad
from pymongo import MongoClient

db_username = "devs"
db_password = "devs"

launchpad = Launchpad.login_anonymously('just testing', 'production')

client = MongoClient("mongodb://{}:{}@localhost/tasks_db".format(db_username, db_password))
lp_db = client["lp_db"] # This is the database
lp_coll = lp_db["lp"] # This is a collection (table) in the database

distro = launchpad.distributions["ubuntu"]

project_list = []

count = 0

with open("db.json", "wb") as f:
    for project in launchpad.projects:
        project_list.append({"name": project.name})
        count += 1
        if count == 100:
            count = 0
            lp_coll.insert_many(project_list)
            project_list = []


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
