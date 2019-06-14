from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
from PackageClass.package import Package

import json


app = Flask(__name__)
CORS(app)

arr = []
newPkg = {}
newPkg["name"] = "test pkg"
package = Package(newPkg)
package._id = '279'
package._version = "128"
package._description = "o descriere a unui nou pachet proaspat realizat inainte de examenul la matlab"
package._maintainer = "any"
package._architecture = "amd64"
arr.append(package)

versionsArray = ["123", "124", "125", "128"]

@app.route("/search", methods = ["GET"])
def getPackageList():
    # if(request.ar)
    # querry_string = request.args['name']
    json_data = {}
    json_data["package_list"] = []
    for package in arr:
        json_data["package_list"].append(package.__dict__)
    return jsonify(json_data)
    
@app.route("/getVersions", methods = ["GET"])
def getVersions():
    if(request.args['id'] is not None):
        id = request.args['id']
        return json.dumps(versionsArray),200, {'Content-Type':'application/json'}
    if(request.args['id'] is None):
        return 'nothing'

@app.route("/getPackage", methods=["GET"])
def getPackage():
    id = request.args['id']
    version = request.args['version']
    package._version = version
    package._id = id
    return json.dumps(package.__dict__), 200, {'Content-Type':'application/json'}

@app.route("/checkout", methods=["POST"])
def checkout():
    print request.data
    return "jsonify(request.data)"

if __name__ == "__main__":
    app.run(host="", port=5123)

    app.debug = True