from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# /search/<pkg_name>
# /package/<pkg_name>/<version*>/<architecture**>
# /install (json with package id list)
@app.route("/search/<pkg_name>", methods=["GET"])
def find_package(pkg_name):
    return list


@app.route("/package/<pkg_name>", methods=["GET"])
def find_package(pkg_name):
    return dict


@app.route("/package/<pkg_name>/<pkg_version>", methods=["GET"])
def find_package(pkg_name, pkg_version):
    return list


@app.route("/package/<pkg_name>/<pkg_version>/<pkg_architecture>", methods=["GET"])
def find_package(pkg_name, pkg_version, pkg_architecture):
    return list


@app.route("/install", methods=["GET"])
def find_package(pkg_name):
    return None


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5121)
