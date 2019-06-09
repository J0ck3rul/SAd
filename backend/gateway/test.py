from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
sys.path.insert(0, '../..')

from package import Package

import json


arr = []
arr.append(Package("firefox"))
arr.append(Package("python"))
arr.append(Package("terminator"))


# if(request.ar)
# querry_string = request.args['name']
json_data = {}
json_data["package_list"] = []
jsonList = []
for package in arr:
    json_data["package_list"].append(package.__dict__)
dict  = arr[1].__dict__
print  json.dumps(json_data)
    

