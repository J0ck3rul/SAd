import difflib
import urllib

from bson.objectid import ObjectId
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, BulkWriteError

from constants import DB_PASSWORD, DB_USERNAME

client = MongoClient("mongodb://{}:{}@localhost/admin".format(DB_USERNAME, DB_PASSWORD))
db = client["sad"]
coll = db["archive-ubuntu"]


def find_packages_by_name(name):
    result = coll.find({
        "name": {
            "$regex": name
        }
    }).distinct("name")
    return difflib.get_close_matches(name, result, 50, 0.5)


def get_package_by_id(pid):
    result = coll.find_one({"_id": ObjectId(pid)})
    result["_id"] = str(result.pop("_id"))
    return result


def get_packages_by_name(name):
    name_fixed = name.replace(":any", "")
    result = list(coll.find({"name": name_fixed}))
    for pkg in result:
        pkg["_id"] = str(pkg.pop("_id"))
    return result


def get_packages_by_name_version(name, version):
    name_fixed = name.replace(":any", "")
    result = list(coll.find({"$and": [
        {"name": name_fixed},
        {"version": version}
    ]}))
    for pkg in result:
        pkg["_id"] = str(pkg.pop("_id"))
    return result


def get_package_by_name_version_arch(name, version, arch):
    name_fixed = name.replace(":any", "")
    print "Getting ", name_fixed, version, arch
    result = coll.find_one({"$and": [
        {"name": name_fixed},
        {"version": version},
        {"architecture": arch}
    ]})
    result["_id"] = str(result.pop("_id"))
    return result


def download_package_by_name_version_arch(name, version, arch):
    name_fixed = name.replace(":any", "")
    result = coll.find_one({"$and": [
        {"name": name_fixed},
        {"version": version},
        {"architecture": arch}
    ]})
    result["_id"] = str(result.pop("_id"))
    deb_url = result["download"]
    response = urllib.urlopen(deb_url)
    return response


def insert_package(package):
    package_obj = package.get_obj()
    try:
        coll.insert_one(package_obj)
    except DuplicateKeyError:
        package_obj.pop("_id")
        coll.find_one_and_update({"$and": [
            {"name": package_obj["name"]},
            {"version": package_obj["version"]}
        ]}, {"$set": package_obj})


def update_packages_database(packages):
    coll.delete_many({})
    try:
        coll.insert_many(packages, ordered=False)
        return True
    except BulkWriteError as e:
        if not any([error["code"] != 11000 for error in e.details["writeErrors"]]):
            return True
        for error in e.details["writeErrors"]:
            if error["code"] != 11000:
                print error["errmsg"]
        raise

