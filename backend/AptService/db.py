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
    if not FindPackageByName(package):
        return packages_coll.insert_one(service.apt_show(package).__repr__()).inserted_id
    else:
        return None   #deja exista acest pachet


def FindPackageByNameAndVersion(package, version):
    obj = list(packages_coll.find({"name": package, "version": version}))
    if obj:
        return obj
    else:
        return None    #nu este gasit pachetul


def FindPackageByName(package):
    obj = list(packages_coll.find({"name": package}))
    if obj:
        return obj
    else:
        return None       #nu este gasit pachetul
