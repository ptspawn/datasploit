try:
    from pip._internal.utils.misc import get_installed_distributions
except ImportError:
    from pip import get_get_installed_distribuitions
import sys


def check_dependency():
    list_deps = []
    missing_deps = []

    with open('requirements.txt') as f:
        list_deps = f.read().splitlines()

    pip_list = sorted([i.key for i in get_installed_distributions()])

    for req_dep in list_deps:
        if req_dep not in pip_list:
            missing_deps.append(req_dep)

    if missing_deps:
        print("You are missing a module for Datasploit. Please install them using: ")
        print("pip install -r requirements.txt")
        sys.exit()
