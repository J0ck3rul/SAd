from json import JSONEncoder, dumps


class Package:
    def __init__(self, package_object):
        self._name = package_object["name"]
        self._id = package_object["_id"] if "_id" in package_object else ""
        self._description = package_object["description"] if "description" in package_object else ""
        self._architecture = package_object["architecture"] if "architecture" in package_object else ""
        self._version = package_object["version"] if "version" in package_object else ""
        self._download = package_object["download"] if "download" in package_object else ""
        self._pre_depends = package_object["pre_depends"] if "pre_depends" in package_object else []
        self._depends = package_object["depends"] if "depends" in package_object else []
        self._conflicts = package_object["conflicts"] if "conflicts" in package_object else []
        self._breaks = package_object["breaks"] if "breaks" in package_object else []
        self._replaces = package_object["replaces"] if "replaces" in package_object else []
        self._installed_size = package_object["installed_size"] if "installed_size" in package_object else -1
        self._download_size = package_object["download_size"] if "download_size" in package_object else -1
        self._homepage = package_object["homepage"] if "homepage" in package_object else ""
        self._maintainer = package_object["maintainer"] if "maintainer" in package_object else ""

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def architecture(self):
        return self._architecture

    @property
    def version(self):
        return self._version

    @property
    def download(self):
        return self._download


    @property
    def dependencies(self):
        return list(self._pre_depends + self._depends)

    @property
    def conflicts(self):
        return list(
            self._conflicts + self._breaks + self._replaces)  # TODO: If X breaks & replaces Y, then Y will be removed and replaced by X by PM

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

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return dumps(self.get_obj(), indent=4)

    def get_obj(self):
        return {
            "name": self._name,
            "description": self._description,
            "architecture": self._architecture,
            "version": self._version,
            "download": self._download,
            "pre_depends": self._pre_depends,
            "depends": self._depends,
            "conflicts": self._conflicts,
            "breaks": self._breaks,
            "replaces": self._replaces,
            "installed_size": self._installed_size,
            "download_size": self._download_size,
            "homepage": self._homepage,
            "maintainer": self._maintainer
        }
