import backend._testing.pmlib


class Package:
    def __init__(self, pkg_as_json):
        self._id = pkg_as_json["_id"]
        self._name = pkg_as_json["name"]
        self._description = pkg_as_json["description"]
        self._version = pkg_as_json["version"]
        self._pre_depends = pkg_as_json["pre depends"]
        self._depends = pkg_as_json["depends"]
        self._conflicts = pkg_as_json["conflicts"]
        self._breaks = pkg_as_json["breaks"]
        self._replaces = pkg_as_json["replaces"]
        self._installed_size = pkg_as_json["installed size"]
        self._download_size = pkg_as_json["download size"]
        self._homepage = pkg_as_json["homepage"]
        self._maintainer = pkg_as_json["maintainer"]
        self._download_link = pkg_as_json["download link"]
        
    @property
    def name(self):
        return self._name
    @property
    def description(self):
        return self._description
    @property
    def version(self):
        return self._version
    @property
    def dependencies(self):
        return list(self._pre_depends + self._depends)
    @property
    def conflicts(self):
        return list(self._conflicts + self._breaks + self._replaces) #TODO: If X breaks & replaces Y, then Y will be removed and replaced by X by PM
    @property
    def installed_size(self):
        return self._installed_size
    @property
    def download_size(self):
        return self._download_size
    @property
    def homepage(self):
        return self._homepage
    @property
    def maintainer(self):
        return self._maintainer
    @property
    def download_link(self):
        return self._download_link
