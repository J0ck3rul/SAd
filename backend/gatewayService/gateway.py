import os
import tempfile

import requests
from flask import Flask, jsonify, send_file
from flask_cors import CORS

from dependencysolver import generate_install_script
from Exceptions import DependencySolvingTimedOutException, ConflictNotResolvedException, PackageNotFoundException

ARCHIVE_UBUNTU_SERVICE_ADDRESS = "http://localhost:5122"
APT_SERVICE_ADDRESS = "http://localhost:5123"
SERVICES = [ARCHIVE_UBUNTU_SERVICE_ADDRESS]


app = Flask(__name__)
CORS(app)


@app.route("/package_id/<pkg_id>", methods=["GET"])
def get_package_by_id(pkg_id):
    for address in SERVICES:
        response = requests.get("{}/package_id/{}".format(address, pkg_id))
        if response.status_code == 200:
            return jsonify(response.json()), 200
    return jsonify({}), response.status_code


@app.route("/search/<pkg_name>", methods=["GET"])
def find_packages_by_name(pkg_name):
    final_result = []
    for address in SERVICES:
        response = requests.get("{}/search/{}".format(address, pkg_name))
        if response.status_code == 200:
            final_result += response.json()
    return jsonify(final_result), 200


@app.route("/package/<pkg_name>", methods=["GET"])
def get_packages_by_name(pkg_name):
    final_result = []
    for address in SERVICES:
        response = requests.get("{}/package/{}".format(address, pkg_name))
        if response.status_code == 200:
            final_result += response.json()
    return jsonify(final_result), 200


@app.route("/package/<pkg_name>/<pkg_version>", methods=["GET"])
def get_packages_by_name_version(pkg_name, pkg_version):
    final_result = []
    for address in SERVICES:
        response = requests.get("{}/package/{}/{}".format(address, pkg_name, pkg_version))
        if response.status_code == 200:
            final_result += response.json()
    return jsonify(final_result), 200


@app.route("/package/<pkg_name>/<pkg_version>/<pkg_architecture>", methods=["GET"])
def get_package_by_name_version_arch(pkg_name, pkg_version, pkg_architecture):
    for address in SERVICES:
        response = requests.get("{}/package/{}/{}/{}".format(address, pkg_name, pkg_version, pkg_architecture))
        if response.status_code == 200:
            return jsonify(response.json()), 200
    return jsonify({}), response.status_code


@app.route("/package/<pkg_name>/<pkg_version>/<pkg_architecture>/download", methods=["GET"])
def download_package_by_name_version_arch(pkg_name, pkg_version, pkg_architecture):
    for address in SERVICES:
        response = requests.get("{}/package/{}/{}/{}/download".format(
            address, pkg_name, pkg_version, pkg_architecture
        ), stream=True)
        if response.status_code == 200:
            return response.raw.read(), response.status_code, response.headers.items()
    return jsonify({}), response.status_code


@app.route("/install/<id_list>", methods=["GET"])
def generate_install_script_route(id_list):
    try:
        id_as_list = id_list.split(",")
        script_str = generate_install_script(id_as_list)
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
    except DependencySolvingTimedOutException:
        return jsonify({"errormsg": "Dependency solving timed out. This can usually happen when the package has a lot of dependencies."}), 408
    except PackageNotFoundException as e:
        return jsonify({"errormsg": "Package not found: {}".format(str(e))}), 404
    except Exception as e:
        return jsonify({"errormsg": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5121)
    app.debug = True
