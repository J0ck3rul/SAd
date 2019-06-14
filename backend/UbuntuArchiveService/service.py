import os
import db
import ubuntuarchive
import apt_pkg


apt_pkg.init_system()


def update_package_db():
    packages = ubuntuarchive.get_all_packages()
    db.update_packages_database(packages)


def get_latest_version_for_package_name(pkg_name, architecture):
    pkgs = db.get_packages_by_name(pkg_name)
    if pkgs:
        versions = [pkg["version"] for pkg in pkgs]
        sortedDict = sorted(versions, cmp=apt_pkg.version_compare, reverse=True)
        return db.get_package_by_name_version_arch(pkg_name, sortedDict[0], architecture)
    else:
        print "Cannot find package ", pkg_name
        return {"version": "N/A"}


def generate_install_script(package_list):
    conflicts_list = []
    dependency_stack_amd64 = []
    dependency_stack_i386 = []
    for pkg in package_list:
        pkg_obj = db.get_package_by_id(pkg)
        if "amd64" == pkg_obj["architecture"]:
            print "Insert " + pkg_obj["name"]
            dependency_stack_amd64.append(pkg_obj["name"])
        elif "i386" == pkg_obj["architecture"]:
            print "Insert " + pkg_obj["name"]
            dependency_stack_i386.append(pkg_obj["name"])
    generate_dependency_stack(dependency_stack_amd64, "amd64")
    generate_dependency_stack(dependency_stack_i386, "i386")
    template_downloader = "wget -O {} http://vvtsoft.ddns.net:5122/package/{}/{}/{}/download"
    template_installer = "echo yes | sudo dpkg -i {}"
    dependency_stack_i386.reverse()
    dependency_stack_amd64.reverse()
    to_install = []

    for pkg_name in dependency_stack_i386:
        pkg_version = get_latest_version_for_package_name(pkg_name, "i386")["version"]
        pkg_obj = db.get_package_by_name_version_arch(pkg_name, pkg_version, "i386")
        download_command = str(template_downloader)
        to_install.append(download_command.format(os.path.join("/tmp", "{}_{}_i386.deb".format(pkg_name, pkg_version)), pkg_name, pkg_version, "i386"))
        install_command = str(template_installer)
        to_install.append(install_command.format(os.path.join("/tmp", "{}_{}_i386.deb".format(pkg_name, pkg_version))))

    for pkg_name in dependency_stack_amd64:
        pkg_version = get_latest_version_for_package_name(pkg_name, "amd64")["version"]
        pkg_obj = db.get_package_by_name_version_arch(pkg_name, pkg_version, "amd64")
        download_command = str(template_downloader)
        to_install.append(download_command.format(os.path.join("/tmp", "{}_{}_amd64.deb".format(pkg_name, pkg_version)), pkg_name, pkg_version, "amd64"))
        install_command = str(template_installer)
        to_install.append(install_command.format(os.path.join("/tmp", "{}_{}_amd64.deb".format(pkg_name, pkg_version))))
    print "#!/bin/bash\nsudo echo Login successful!\n" + "\n".join(to_install)
    return "#!/bin/bash\n" + "\n".join(to_install)


def generate_dependency_stack(dependency_stack, arch):
    cycle_deps = []
    stack_pos = [0, 0]
    while stack_pos[0] < len(dependency_stack):
        pkg = get_latest_version_for_package_name(
            dependency_stack[stack_pos[0]],
            arch
        )
        if "depends" in pkg:
            for depend in pkg["depends"]:
                depend_name = depend.split(" ")[0].replace(":all", "")
                if depend_name in cycle_deps:
                    print "Skip cycle " + depend_name
                    continue
                print "Insert " + depend_name
                place_dependency_in_stack(dependency_stack, depend_name, stack_pos)
                print dependency_stack
                if stack_pos[1] > len(dependency_stack)*2:
                    cycle_deps.append(depend_name)
                    stack_pos[1] = 0
        stack_pos[0] += 1


def place_dependency_in_stack(dependency_stack, new_depend_name, stack_pos):
    depend = None
    for temp_depend in dependency_stack:
        if temp_depend == new_depend_name:
            depend = temp_depend
    if depend is None:
        dependency_stack.append(new_depend_name)
        stack_pos[1] = 0
        return
    if dependency_stack.index(depend) < stack_pos[0]:  # If we find the dependency before the current element, move it to the front
        # print "Move"
        dependency_stack.remove(depend)
        stack_pos[0] -= 1
        stack_pos[1] += 1
        dependency_stack.append(depend)
        # Check if the dependency is compatible the new one and change it accordingly if necessary

# update_package_db()
# print generate_install_script(["5d02e5af10ecd1083bf2ed04"])

