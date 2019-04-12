from getto.constants import *
from launchpadlib.launchpad import Launchpad

launchpad = Launchpad.login_anonymously('just testing', 'production')

def find_project(pkg_name):
    results = []
    for result in launchpad.projects.search(text=pkg_name):
        if pkg_name in result.name:
            results.append(result)
            if pkg_name == result.name:
                return result
    return results