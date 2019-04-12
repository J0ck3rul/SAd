import getto

# print getto.get_all_distros()
# getto.pull_all_packages_into_db()

for binary in getto.get_package_binaries("firefox", "ubuntu", "bionic", "amd64"):
    print binary.self_link
# http://launchpadlibrarian.net/416686702/firefox_66.0.2+build1-0ubuntu0.18.04.1_amd64.deb