from flask import Flask, request, jsonify

import sys
sys.path.insert(0, '../..')

from package import Package

import json


app = Flask(__name__)

arr = []
arr.append(Package("firefox"))
arr.append(Package("python"))
arr.append(Package("terminator"))


@app.route("/search", methods = ["GET"])
def hello():
    querry_string = request.args['name']
    jsonList = []
    for package in arr:
        jsonList.append(json.dumps(package.__dict__))
    dict  = arr[1].__dict__
    return jsonify(jsonList)
    



if __name__ == "__main__":
    app.run(host="", port=5123)

    app.debug = True