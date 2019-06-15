import db
import apt_pkg


SYMBOL_TO_COMPARISON_RESULT_TABLE = {
    ">= ": []
}


def get_install_order_for_dependency_list(dep_list):
    pass

# dep_list = {"name", "version"}, final_dep_list = {"name", "version_list"}
def dependency_list_validation(dep_list):
    final_dep_list = []
    for dep_to_insert in dep_list:
        for dep_matched in final_dep_list:
            if dep_to_insert["name"] == dep_matched["name"]:
                concatenate_dependencies(dep_to_insert, dep_matched)
                break


def concatenate_dependencies(inserted_dep, existing_dep):
    if ">= " in inserted_dep:


def apply_filter_on_versions(version_list, filter):
    for version in version_list:
        if ">= " == filter[0:3]:
