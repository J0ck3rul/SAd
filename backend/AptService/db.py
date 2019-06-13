import os
import sys

sys.path.insert(0, os.path.abspath('..'))
from PackageClass.package import Package
from pymongo import MongoClient
from bson.objectid import ObjectId
import service

db_username = "sad"
db_password = "sad"

client = MongoClient("mongodb://{}:{}@localhost/admin".format(db_username, db_password))
db = client["sad"]
packages_coll = db["packages"]


def InsertDB(package):
    if not GetPackageByName(package):
        return packages_coll.insert_one(service.apt_show(package).__repr__()).inserted_id
    else:
        return None  # deja exista acest pachet


def GetPackageByNameAndVersion(package, version):
    obj = list(packages_coll.find({"name": package, "version": version}))
    if obj:
        pkg = Package(obj[0])
        return pkg
    else:
        return None


def GetPackageByName(package):
    obj_list = list(packages_coll.find({"name": package}))
    pkg_list = []
    for obj in obj_list:
        pkg = Package(obj)
        pkg_list.append(pkg)
    return pkg_list


 InsertDB("python")

# print GetPackageByName("python")
