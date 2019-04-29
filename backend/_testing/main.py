from pmlib.aptlib import apt_show


x=apt_show("python")
for key in x.__dict__:
    print("{}: {}".format(key,x.__dict__[key]))