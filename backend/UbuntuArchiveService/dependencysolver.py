import db
import apt_pkg


SYMBOL_TO_COMPARISON_RESULT_TABLE = {
    ">> ": [1],
    "= ": [0],
    "<<": [-1],
    ">= ": [0, 1],
    "<= ": [0, -1]
}


def version_comparison(a, b):
    comp_result = apt_pkg.version_compare(a, b)
    if comp_result > 0:
        return 1
    if comp_result < 0:
        return -1
    return 0


def is_version_in_dependency(dependency, ver):
    for symbol in SYMBOL_TO_COMPARISON_RESULT_TABLE:
        if symbol == dependency[0:len(symbol)+1]:
            dep_vers = dependency.replace(symbol, "")
            comp_result = version_comparison(dep_vers, ver)
            if comp_result in SYMBOL_TO_COMPARISON_RESULT_TABLE[symbol]:
                return True
            return False
    raise ValueError("Dependency format not recognised")


def get_install_order_for_dependency_list(dep_list):
    pass


def populate_dependency_list(dep_list):
    final_dep_list = []
    for dep_to_insert in dep_list:
        for dep_matched in final_dep_list:
            if dep_to_insert["name"] == dep_matched["name"]:
                concatenate_dependencies(dep_to_insert, dep_matched)
                break


def get_dependency_list_from_package(pkg):
    for dep in pkg["pre_depends"]:


