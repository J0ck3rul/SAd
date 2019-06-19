DB_USERNAME = "sad"
DB_PASSWORD = "sad"

SERVER_PUBLIC_ADDRESS = "http://vvtsoft.ddns.net:5122"

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
