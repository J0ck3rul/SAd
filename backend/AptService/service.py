import aptlib
import json
from flask import Flask, jsonify
from flask import request
from flask import make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# get pkg by name
# find pkg by name
# get pkg deb by name
# generate install script


@app.route("/search/<pkg_name>", methods=["GET"])
def find_packages_by_name(pkg_name):
    try:
        return jsonify(aptlib.apt_search(pkg_name)), 200
    except Exception as e:
        return jsonify({"errormsg": str(e)}), 404


@app.route("/package/<pkg_name>", methods=["GET"])
def get_packages_by_name(pkg_name):
    try:
        return jsonify(aptlib.apt_show(pkg_name)), 200
    except Exception as e:
        print "Da"
        return jsonify({"errormsg": str(e)}), 404


@app.route("/package/<pkg_name>/<pkg_version>", methods=["GET"])
def get_packages_by_name_version(pkg_name, pkg_version):
    try:
        return jsonify(aptlib.apt_show_by_version(pkg_name, pkg_version)), 200
    except Exception as e:
        return jsonify({"errormsg": str(e)}), 404


@app.route("/package/<pkg_name>/<pkg_version>/<pkg_architecture>", methods=["GET"])
def get_package_by_name_version_arch(pkg_name, pkg_version, pkg_architecture):
    try:
        return jsonify(aptlib.apt_show_by_version_arch(pkg_name, pkg_version, pkg_architecture)), 200
    except Exception as e:
        return jsonify({"errormsg": str(e)}), 404


@app.route("/package/<pkg_name>/<pkg_version>/<pkg_architecture>/download", methods=["GET"])
def download_package_by_name_version_arch(pkg_name, pkg_version, pkg_architecture):
    try:
        return send_file(
            db.download_package_by_name_version_arch(pkg_name, pkg_version, pkg_architecture),
            "application/vnd.debian.binary-package",
            as_attachment=True,
            attachment_filename="{}_{}_{}.deb".format(pkg_name, pkg_version, pkg_architecture)
        ), 200
    except Exception as e:
        return jsonify({"errormsg": str(e)}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5121)
