import db

from flask import Flask
from flask import request
from flask import make_response
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
#get pkg by name
#find pkg by name
#get pkg deb by name
#generate install script




@app.route("/<task_id>", methods = ["GET"])
def get_pkg_by_name(task_id):
    return db.getById(task_id)

@app.route("/<task_id>", methods = ["GET"])
def get_task_by_id(task_id):
    return db.getById(task_id)

@app.route("/<task_id>", methods = ["GET"])
def get_task_by_id(task_id):
    return db.getById(task_id)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5121)