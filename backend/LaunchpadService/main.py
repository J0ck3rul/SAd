import db
import ubuntuarchive


def update_package_db():
    packages = ubuntuarchive.get_all_packages()
    db.update_packages_database(packages)


update_package_db()

