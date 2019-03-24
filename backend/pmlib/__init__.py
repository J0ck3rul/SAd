# Aici vom face diferentierea intre sistemele de operare
# Practic, asta e o abstractizare, pentru ca atunci cand importam
# pmlib, scriptul init va importa doar functiile corespunzatoare
# sistemului de operare pe care ruleaza
import platform

PACKAGE_MANAGERS = {
    "apt": ["debian", "ubuntu"],
    "yum": ["fedora"]
}

if platform.linux_distribution()[0] in PACKAGE_MANAGERS["apt"]:
    import aptlib as packagemanager
elif platform.linux_distribution()[0] in PACKAGE_MANAGERS["yum"]:
    import yumlib as packagemanager
else:
    raise Exception("Distribution not supported!\nCheck the supported distro list on our website. ;)")
