from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

import os
import db
import service
import tempfile

app = Flask(__name__)
CORS(app)


# /search/<pkg_name>
# /package/<pkg_name>/<version*>/<architecture**>
# /install (json with package id list)
@app.route("/search/<pkg_name>", methods=["GET"])
def find_packages_by_name(pkg_name):
    try:
        return jsonify(db.find_packages_by_name(pkg_name)), 200
    except Exception as e:
        return jsonify({"errormsg": str(e)}), 404


@app.route("/package/<pkg_name>", methods=["GET"])
def get_packages_by_name(pkg_name):
    try:
        return jsonify(db.get_packages_by_name(pkg_name)), 200
    except Exception as e:
        return jsonify({"errormsg": str(e)}), 404


@app.route("/package/<pkg_name>/<pkg_version>", methods=["GET"])
def get_packages_by_name_version(pkg_name, pkg_version):
    try:
        return jsonify(db.get_packages_by_name_version(pkg_name, pkg_version)), 200
    except Exception as e:
        return jsonify({"errormsg": str(e)}), 404


@app.route("/package/<pkg_name>/<pkg_version>/<pkg_architecture>", methods=["GET"])
def get_package_by_name_version_arch(pkg_name, pkg_version, pkg_architecture):
    try:
        return jsonify(db.get_package_by_name_version_arch(pkg_name, pkg_version, pkg_architecture)), 200
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


@app.route("/install/<id_list>", methods=["GET"])
def generate_install_script(id_list):
    # try:
    id_as_list = id_list.split(",")
    print id_as_list
    script_str = service.generate_install_script(id_as_list)
    temp_dir = tempfile.mkdtemp()
    with open(os.path.join(temp_dir, "install.sh"), "wb") as f:
        f.write(script_str)
    return send_file(
        os.path.join(temp_dir, "install.sh"),
        "application/x-sh",
        as_attachment=True,
        attachment_filename="install.sh",
        cache_timeout=-1
    ), 200
    # except Exception as e:
    #     return jsonify({"errormsg": str(e)}), 404


@app.route("/rebuild_db", methods=["GET"])
def rebuild_db():
    try:
        service.update_package_db()
    except Exception as e:
        return jsonify({"errormsg": str(e)}), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5122)

# http://localhost:5000/search/nano
# http://localhost:5000/package/nano
# http://localhost:5000/package/nano/2.9.8-1
# http://localhost:5000/package/nano/2.9.8-1/amd64
# http://localhost:5000/package/nano/2.9.8-1/amd64/download
# http://localhost:5000/install
