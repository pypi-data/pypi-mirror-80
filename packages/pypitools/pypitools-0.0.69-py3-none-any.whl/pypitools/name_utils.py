import os
import subprocess

from pypitools.configs import ConfigData


def get_package_fullname() -> str:
    """
    Get the full name of the package
    """
    return (
        subprocess.check_output(
            [ConfigData.python, "setup.py", "--fullname"]
        )
        .decode()
        .rstrip()
    )


def get_package_filename() -> str:
    """
    Get the package filename
    """
    return os.path.join("dist", get_package_fullname() + ".tar.gz")


def get_package_wheelname() -> str:
    """
    Get the package wheelname
    """
    return os.path.join("dist", get_package_fullname() + "-py3-none-any.whl")
