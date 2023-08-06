import os
import sys
from subprocess import check_call, CalledProcessError


def checkinstallation():
    from . import checkInstallationIP


def recuparchives():
    from . import recupArchives


def import_data():
    from . import import_data


def export_data():
    from . import export_data


def rename():
    from . import change_name


def remove_ldap():
    from . import remove_ldap


def pushdoc():
    from . import pushdoc


def ipclean():
    from . import ipclean


def ldapsearch():
    from . import ldapsearch


def count_files():
    from . import count_files


def reset_admin_password():
    from . import reset_admin_password


def patch():
    from . import patch


def properties_merger():
    args = sys.argv[1:]
    args.insert(0, os.path.dirname(os.path.realpath(__file__)) + "/shell/properties-merger/properties-merger.sh")
    try:
        check_call(args)
    except CalledProcessError:
        pass
