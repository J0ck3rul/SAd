from constants import DB_PASSWORD, DB_USERNAME
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, BulkWriteError
from bson.objectid import ObjectId

client = MongoClient("mongodb://{}:{}@localhost/admin".format(DB_USERNAME, DB_PASSWORD))
db = client["sad"]
coll = db["archive-ubuntu"]


def get_package_by_id(pid):
    result = coll.find_one({"_id": ObjectId(pid)})
    return result


def get_packages_by_name(name):
    result = coll.find({"name": name})
    return list(result)


def get_package_by_name_and_version(name, version):
    result = coll.find_one({"$and": [
        {"name": name},
        {"version": version}
    ]})
    return result


def insert_package(package):
    package_obj = package.get_obj()
    try:
        coll.insert_one(package_obj)
    except DuplicateKeyError as e:
        package_obj.pop("_id")
        coll.find_one_and_update({"$and": [
            {"name": package_obj["name"]},
            {"version": package_obj["version"]}
        ]}, {"$set": package_obj})


def update_packages_database(packages):
    coll.delete_many({})
    package_objects = [package.get_obj() for package in packages]
    try:
        coll.insert_many(package_objects, ordered=False)
    except BulkWriteError as e:
        print e.details

