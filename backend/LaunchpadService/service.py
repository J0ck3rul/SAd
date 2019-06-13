import db
import ubuntuarchive


def update_package_db():
    packages = ubuntuarchive.get_all_packages()
    db.update_packages_database(packages)


def generate_install_script(package_list):
    dependency_stack = []
    


# update_package_db()

