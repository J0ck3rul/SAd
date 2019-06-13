import difflib

from constants import DB_PASSWORD, DB_USERNAME
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, BulkWriteError
from bson.objectid import ObjectId

client = MongoClient("mongodb://{}:{}@localhost/admin".format(DB_USERNAME, DB_PASSWORD))
db = client["sad"]
coll = db["archive-ubuntu"]


def find_package_by_name(name):
    result = coll.find({
        "name": {
            "$regex": name
        }
    })
    return difflib.get_close_matches(name, [package["name"] for package in result], 50, 0.5)


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
    try:
        package_objects = [package.get_obj() for package in packages]
        coll.insert_many(package_objects, ordered=False)
        return True
    except BulkWriteError as e:
        with [error["code"] != 11000 for error in e.details["writeErrors"]] as error_code_check_list:
            if not any(error_code_check_list):
                return True
        for error in e.details["writeErrors"]:
            if error["code"] != 11000:
                print error["errmsg"]
        raise

