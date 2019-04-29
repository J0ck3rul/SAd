# Aici vom face diferentierea intre sistemele de operare
# Practic, asta e o abstractizare, pentru ca atunci cand importam
# pmlib, scriptul init va importa doar functiile corespunzatoare
# sistemului de operare pe care ruleaza
import platform

PACKAGE_MANAGERS = {
    "apt": {
        "debian": ["9.8"],
        "ubuntu": ["16.04", "17.04", "17.10", "18.04", "18.10"]
    },
    "yum": {
        "fedora": ["29"]
    }
}

CURRENT_DISTRO = platform.linux_distribution()[0]
CURRENT_VERSION = platform.linux_distribution()[1]

if CURRENT_DISTRO in PACKAGE_MANAGERS["apt"] and CURRENT_VERSION in PACKAGE_MANAGERS["apt"][CURRENT_DISTRO]:
    import aptlib as packagemanager
elif CURRENT_DISTRO in PACKAGE_MANAGERS["yum"] and CURRENT_VERSION in PACKAGE_MANAGERS["yum"][CURRENT_DISTRO]:
    import yumlib as packagemanager
else:
    # raise Exception("Distribution not supported!\nCheck the supported distro list on our website. ;)") #TODO: Needs to be removed in production
    pass
