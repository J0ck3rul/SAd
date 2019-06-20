import json
import re
import apt_pkg
import requests


GATEWAY_SERVICE_ADDRESS = "http://localhost:5121"


apt_pkg.init_system()


SYMBOL_TO_COMPARISON_RESULT_TABLE = {
    ">>": [1],
    "=": [0],
    "<<": [-1],
    ">=": [0, 1],
    "<=": [0, -1]
}


def get_packages_by_name(pkg_name):
    response = requests.get("{}/package/{}".format(GATEWAY_SERVICE_ADDRESS, pkg_name))
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_package_by_id(pkg_id):
    response = requests.get("{}/package_id/{}".format(GATEWAY_SERVICE_ADDRESS, pkg_id))
    if response.status_code == 200:
        return response.json()
    else:
        return None


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
    packages_found = get_packages_by_name(dependency["name"])
    matching_packages = []
    for package in packages_found:
        if dependency["name"] == package["name"] and \
            (dependency["architecture"] == "any" or \
             dependency["architecture"] == package["architecture"]):
            if dependency["condition"] in SYMBOL_TO_COMPARISON_RESULT_TABLE and \
                version_comparison(package["version"], dependency["version"]) in \
                    SYMBOL_TO_COMPARISON_RESULT_TABLE[dependency["condition"]]:
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
        comp_result = version_comparison(ver, dep_version)
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
    # This iteration finds all possible dependency packages and bundles them all together, separated list of strict dependencies
    first_deps_list = list(packages)
    grouped_deps = {}

    for dep in first_deps_list:
        grouped_deps[dep["name"]] = [dep]

    keep_running = True
    new_additions = list(first_deps_list)
    new_list = []
    while keep_running or new_list:
        new_additions_grouped = {}
        keep_running = False
        new_list = []
        for pkg in new_additions:
            for new_dependency in get_packages_matching_dependencies_for_package(pkg):
                if new_dependency["name"] not in new_additions_grouped:
                    new_additions_grouped[new_dependency["name"]] = []
                if new_dependency not in new_additions_grouped[new_dependency["name"]]:
                    new_additions_grouped[new_dependency["name"]].append(new_dependency)
                    new_additions.append(new_dependency)

        for pkg_name in new_additions_grouped:
            if pkg_name in grouped_deps.keys():
                new_group = \
                    [
                        json.loads(pkg_str) for pkg_str in
                        (
                            set(
                                [json.dumps(pkg_obj, sort_keys=True) for pkg_obj in grouped_deps[pkg_name]]
                            ).intersection(
                                set(
                                    [json.dumps(pkg_obj, sort_keys=True) for pkg_obj in new_additions_grouped[pkg_name]]
                                )
                            )
                        )
                    ]
                if new_group != grouped_deps[pkg_name]:
                    grouped_deps[pkg_name] = new_group
                    keep_running = True
            else:
                grouped_deps[pkg_name] = new_additions_grouped[pkg_name]
                keep_running = True
        new_additions = list(new_list)
    return grouped_deps


# Dependency backtracking #
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
    for pkg in package_list:
        if "depends" in pkg:
            for dep in pkg["depends"]:
                this_dep_obj_list = get_dependency_objects_list(dep, pkg["architecture"])
                found_dep = False
                for dep_obj in this_dep_obj_list:
                    for pkg in package_list:
                        if dep_obj["name"] == pkg["name"]:
                            if is_version_in_dependency(dep_obj, pkg["version"]):
                                found_dep = True
                                break
                if not found_dep:
                    return False
    return True
# Dependency backtracking #


def second_iteration(packages):
    # This iteration recurses every distinct package name, using backtracking,
    # trying to match them such that all dependencies are satisfied
    grouped_packages = packages
    packages_to_install = []
    if dependency_bkt(0, [pkg_name for pkg_name in grouped_packages], grouped_packages, packages_to_install):
        return packages_to_install
    return False


def get_dependency_list_for_packages(pkg_list):
    final_list = first_iteration(pkg_list)
    result = second_iteration(final_list)
    return result


def generate_install_script(package_ids_list):
    conflicts_list = []
    package_list = []
    for pkg_id in package_ids_list:
        pkg_obj = get_package_by_id(pkg_id)
        package_list.append(pkg_obj)
    pkgs_to_install_list = get_dependency_list_for_packages(package_list)
    template_downloader = "wget -O {0}_{1}_{2}.deb {3}/package/{0}/{1}/{2}/download >/dev/null 2>&1\n"
    template_pkg_name = "{}_{}_{}.deb"
    template_installer = "echo yes | sudo dpkg -i {} || exit\n"

    file_content = "#!/bin/bash\n\n"
    for pkg in pkgs_to_install_list:
        file_content += str(template_downloader).format(
            pkg["name"], pkg["version"], pkg["architecture"], GATEWAY_SERVICE_ADDRESS
        )
    file_content += str(template_installer).format(
        " ".join(
            [str(template_pkg_name).format(
                pkg["name"], pkg["version"], pkg["architecture"]
            ) for pkg in pkgs_to_install_list]
        )
    )
    return file_content

