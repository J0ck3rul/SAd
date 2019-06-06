from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
sys.path.insert(0, '../..')

from package import Package

import json


app = Flask(__name__)
CORS(app)

arr = []
arr.append(Package("firefox"))
arr.append(Package("python"))
arr.append(Package("terminator"))
package = Package("new pkg")
package._id = '279'
package._version = "128"
package._description = "o descriere a unui nou pachet proaspat realizat inainte de examenul la matlab"
package._maintainer = "any"
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
    return json.dumps(json_data), 200, {'Content-Type':'application/json'}
    
@app.route("/getVersions", methods = ["GET"])
def getVersions():
    if(request.args['id'] is not None):
        id = request.args['id']
        return json.dumps(versionsArray),200, {'Content-Type':'application/json'}
    if(request.args['id'] is None):
        return 'nothing'


if __name__ == "__main__":
    app.run(host="", port=5123)

    app.debug = True