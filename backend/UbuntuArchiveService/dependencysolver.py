import db
import re
import apt_pkg


apt_pkg.init_system()


SYMBOL_TO_COMPARISON_RESULT_TABLE = {
    ">>": [1],
    "=": [0],
    "<<": [-1],
    ">=": [0, 1],
    "<=": [0, -1]
}


# Dependency filtered getter #
def get_dependency_objects_list(dep, arch):
    dependency_list = [dep]
    if " | " in dep: # Dep is a list of dependencies
        dependency_list = dep.split(" | ")

    dep_obj_list = []
    for dependency in dependency_list:
        pkg_name_version_arch_match = re.findall(r"^([^ ]*):([^ ]*)\ \(([<=>]*)\ (.+)\)$", dependency)
        pkg_name_arch_match = re.findall(r"^([^ ]*):([^ ]*)$", dependency)
        pkg_name_version_match = re.findall(r"^([^ ]*)\ \(([<=>]*)\ (.+)\)$", dependency)
        pkg_name_match = re.findall(r"^([^ ]*)$", dependency)
        dep_obj = {}
        if pkg_name_version_arch_match:
            dep_obj["name"] = pkg_name_version_arch_match[0][0]
            dep_obj["architecture"] = pkg_name_version_arch_match[0][1]
            dep_obj["condition"] = pkg_name_version_arch_match[0][2]
            dep_obj["version"] = pkg_name_version_arch_match[0][3]
        elif pkg_name_arch_match:
            dep_obj["name"] = pkg_name_arch_match[0][0]
            dep_obj["architecture"] = pkg_name_arch_match[0][1]
            dep_obj["condition"] = ">>"
            dep_obj["version"] = "0"
        elif pkg_name_version_match:
            dep_obj["name"] = pkg_name_version_match[0][0]
            dep_obj["architecture"] = arch
            dep_obj["condition"] = pkg_name_version_match[0][1]
            dep_obj["version"] = pkg_name_version_match[0][2]
        elif pkg_name_match:
            dep_obj["name"] = pkg_name_match[0]
            dep_obj["architecture"] = arch
            dep_obj["condition"] = ">>"
            dep_obj["version"] = "0"
        else:
            continue
        dep_obj_list.append(dep_obj)
    return dep_obj_list


def get_packages_matching_dependency(dependency):
    packages_found = db.get_packages_by_name(dependency["name"])
    matching_packages = []
    for package in packages_found:
        if dependency["name"] == package["name"] and \
            (dependency["architecture"] == "any" or \
             dependency["architecture"] == package["architecture"]):
            if dependency["condition"] in SYMBOL_TO_COMPARISON_RESULT_TABLE and \
                version_comparison(package["version"], dependency["version"]) in SYMBOL_TO_COMPARISON_RESULT_TABLE[dependency["condition"]]:
                matching_packages.append(package)
    return matching_packages


def version_comparison(a, b):
    comp_result = apt_pkg.version_compare(a, b)
    if comp_result > 0:
        return 1
    if comp_result < 0:
        return -1
    return 0


def is_version_in_dependency(dependency, ver):
    dep_condition = dependency["condition"]
    dep_version = dependency["version"]

    if dep_condition in SYMBOL_TO_COMPARISON_RESULT_TABLE:
        comp_result = version_comparison(dep_version, ver)
        if comp_result in SYMBOL_TO_COMPARISON_RESULT_TABLE[dep_condition]:
            return True
        return False
    raise ValueError("Dependency format not recognised")


def get_packages_matching_dependencies_for_package(pkg):
    matching_packages_list = []
    if "depends" in pkg:
        for dependency in pkg["depends"]:
            for dep_obj_test in get_dependency_objects_list(dependency, pkg["architecture"]):
                for matching_pkg in get_packages_matching_dependency(dep_obj_test):
                    matching_packages_list.append(matching_pkg)
    return matching_packages_list
# Dependency filtered getter #


def first_iteration(packages):
    # This iteration finds all possible dependency packages and bundles them all together
    first_deps_list = list(packages)
    first_run = True
    new_additions = list(first_deps_list)
    new_list = []
    while first_run or new_list:
        first_run = False
        new_list = []
        for pkg in new_additions:
            for new_dependency in get_packages_matching_dependencies_for_package(pkg):
                if new_dependency not in first_deps_list and new_dependency not in new_list:
                    new_list.append(new_dependency)
        first_deps_list += new_list
        new_additions = list(new_list)
    return first_deps_list


# Dependency backtracking #
def group_packages_by_name(pkg_list):
    grouped_pkgs = {}
    for pkg in pkg_list:
        if pkg["name"] not in grouped_pkgs:
            grouped_pkgs[pkg["name"]] = [pkg]
        else:
            grouped_pkgs[pkg["name"]].append(pkg)
    return grouped_pkgs


def dependency_bkt(pkg_index, pkg_names_list, grouped_packages, chosen_packages):
    if pkg_index == len(pkg_names_list):
        return check_all_dependencies_satisfied(chosen_packages)
    for pkg in grouped_packages[pkg_names_list[pkg_index]]:
        chosen_packages.append(pkg)
        if dependency_bkt(pkg_index+1, pkg_names_list, grouped_packages, chosen_packages):
            return True
        chosen_packages.remove(pkg)
    return False


def check_all_dependencies_satisfied(package_list):
    return True
# Dependency backtracking #


def second_iteration(packages):
    # This iteration recurses every distrinct package name, using backtracking, trying to match them such that all dependencies are satisfied
    grouped_packages = group_packages_by_name(packages)
    packages_to_install = []
    if dependency_bkt(0, [pkg_name for pkg_name in grouped_packages], grouped_packages, packages_to_install):
        return packages_to_install
    return False


final_list = first_iteration([db.get_package_by_name_version_arch("python", "2.7.5-5ubuntu3", "amd64")])
# print second_iteration(final_list)
for elem in second_iteration(final_list):
    print elem["name"], elem["version"], elem["architecture"]
# for elem in final_list:
#     print elem["name"], elem["version"], elem["architecture"]
# print len(final_list), "elements"
# print group_packages_by_name(final_list)
