import os
import sys

sys.path.insert(0, os.path.abspath('..'))
from PackageClass.package import Package
from pymongo import MongoClient
from bson.objectid import ObjectId
import service
import aptlib

db_username = "sad"
db_password = "sad"

client = MongoClient("mongodb://{}:{}@localhost/admin".format(db_username, db_password))
db = client["sad"]
packages_coll = db["packages"]


def InsertDB(package):
    if not get_packages_by_name(package):
        return packages_coll.insert_one(aptlib.apt_show(package))
    else:
        return None  # deja exista acest pachet


def get_package_by_id(pid):
    result = packages_coll.find_one({"_id": ObjectId(pid)})
    if not result:
        return None
    else:
        result["_id"] = str(result.pop("_id"))
        return result


def get_packages_by_name(name):
    obj = packages_coll.find_one({"name": name})
    if obj:
        obj["_id"] = str(obj["_id"])
        return obj
    else:
        return None

#
# def get_packages_by_name_version(name, version):
#     obj = packages_coll.find_one({"name": name, "version": version})
#     if obj:
#         return obj
#     else:
#         return None


# def GetPackageByNameAndVersion(package, version):
#     obj = list(packages_coll.find({"name": package, "version": version}))
#     if obj:
#         pkg = Package(obj[0])
#         return pkg
#     else:
#         return None
#
#
# def GetPackageByName(package):
#     obj_list = list(packages_coll.find({"name": package}))
#     pkg_list = []
#     for obj in obj_list:
#         pkg = Package(obj)
#         pkg_list.append(pkg)


# print get_package_by_id("5d0b5c11780e6c0154144ce9")
print get_packages_by_name("nano")
# print get_packages_by_name_version("nano","2.9.3-2")

# print GetPackageByName("python")
