DB_USERNAME = "devs"
DB_PASSWORD = "devs"

PKG_CONTENT_MATCHES = {
    r"^Package: (.+)$": "name",
    r"^Description: (.+)$": "description",
    r"^Architecture: (.+)$": "arch",
    r"^Version: (.+)$": "version",
    r"^Maintainer: (.+)$": "maintainer",
    r"^Installed-Size: (.+)$": "installed_size",  # in KB
    r"^Depends: (.+)$": "depends",
    r"^Filename: (.+)$": "download",
    r"^Size: (.+)$": "download_size",  # in B
    r"^Homepage: (.+)$": "homepage",
    r"^Pre-Depends: (.+)$": "pre_depends",
    r"^Conflicts: (.+)$": "conflicts",
    r"^Breaks: (.+)$": "breaks",
    r"^Replaces: (.+)$": "replaces"
}
