from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
from PackageClass.package import Package

import json


app = Flask(__name__)
CORS(app)

arr = []
arr2 = []
newPkg = {}
newPkg["name"] = "test pkg"
package = Package(newPkg)
package._id = '279'
package._version = "128"
package._description = "o descriere a unui nou pachet proaspat realizat inainte de examenul la matlab"
package._maintainer = "any"
package._architecture = "amd64"

package2 = Package(newPkg)
package2._id = '210'
package2._version = "129"
package2._description = "o descriere a unui nou pachet proaspat realizat inainte de examenul la matlab"
package2._maintainer = "any"
package2._architecture = "x86"

arr2.append(package)
arr2.append(package2)
arr2.append(package)
arr = [
    "nano",
    "nanoc",
    "nanook",
    "nanoweb",
    "nanourl",
    "deepnano",
    "nanoc-doc",
    "nano-tiny",
    "nanopolish",
    "nanoweb-doc",
    "nanoblogger",
    "libnanomsg5",
    "libnanomsg4",
    "libnanomsg0",
    "libnanohttp1"
]


versionsArray = ["123", "124", "125", "128"]

@app.route("/search", methods = ["GET"])
def getPackageList():
    # if(request.ar)
    # querry_string = request.args['name']
    json_data = {}
    json_data = arr
    return jsonify(json_data)

@app.route("/package", methods= ["GET"])
def getPackage():
    name = request.args['name']
    json_data = []

    for package in arr2:
        json_data.append(package.__dict__)
    return jsonify(json_data)

@app.route("/getPackage", methods = ["GET"])
def getVersions():
    name = request.args["name"]
    version = request.args["version"]
    architecture = request.args["architecture"]
    return jsonify(package2.__dict__)
# @app.route("/getPackage", methods=["GET"])
# def getPackage():
#     id = request.args['id']
#     version = request.args['version']
#     package._version = version
#     package._id = id
#     return json.dumps(package.__dict__), 200, {'Content-Type':'application/json'}

@app.route("/checkout", methods=["POST"])
def checkout():
    # print request.data
    return send_file("__init__.py")

if __name__ == "__main__":
    app.run(host="", port=5123)

    app.debug = True