import os
import sys
sys.path.insert(0, os.path.abspath('..'))
from PackageClass.package import Package

import db
import lplib
import debdownloader
import ubuntuarchive


def update_package_db():
    packages = ubuntuarchive.get_all_packages()
    db.update_packages_database(packages)


update_package_db()

