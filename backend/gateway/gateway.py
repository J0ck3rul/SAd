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
    return jsonify(arr)
    



if __name__ == "__main__":
    app.run(host="", port=5123)
    app.debug = True