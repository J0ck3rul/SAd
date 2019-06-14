from copy import deepcopy
import db
import ubuntuarchive
import apt_pkg

apt_pkg.init_system()


def compare_versions(a, b):
    return apt_pkg.version_compare(a, b)

def check_vers_depend(version, dependency_version):
    split_str = dependency_version.split(" ")
    operation, dependency_version =


def update_package_db():
    packages = ubuntuarchive.get_all_packages()
    db.update_packages_database(packages)


# Dependency format {"name", "min_version", "max_version"}
def generate_install_script(package_list):
    conflicts_list = []
    dependency_stack = []
    for pkg in package_list:
        pkg_obj = db.get_package_by_id(pkg)
        dependency_stack.append({
            "name": pkg_obj["name"]
        })
    generate_dependency_stack(dependency_stack)


def generate_dependency_stack(dependency_stack):
    stack_pos = [0]
    while stack_pos[0] < len(dependency_stack):
        pkg = db.get_package_by_id(dependency_stack[stack_pos[0]]["_id"])
        for depend_name in pkg["depends"]:

            place_dependency_in_stack(dependency_stack, depend, stack_pos)


def place_dependency_in_stack(dependency_stack, new_depend, stack_pos):
    depend = None
    for temp_depend in dependency_stack:
        if depend["name"] == new_depend["name"]:
            depend = temp_depend
    if not depend:
        return
    if dependency_stack.index(depend) < stack_pos[0]:  # If we find the dependency before the current element, move it to the front
        dependency_stack.remove(depend)
        stack_pos[0] -= 1
        dependency_stack.append(depend)
        # Check if the dependency is compatible the new one and change it accordingly if necessary


def get_depend_interval(depend):

    split_str = depend[""]




    


# update_package_db()

