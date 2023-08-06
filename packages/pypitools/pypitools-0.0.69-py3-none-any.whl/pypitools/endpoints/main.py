"""
main entry point to the program
"""
import os
import shutil
import subprocess

import pylogconf.core

from pypitools.configs import ConfigData
from pypitools.version import VERSION_STR, DESCRIPTION
from pytconf import register_main, config_arg_parse_and_launch, register_endpoint

import pypitools
from pypitools.common import clean_before_if_needed, package_it, check_if_needed, upload_select,\
    clean_after_if_needed, \
    register_select, do_prerequisites
from pypitools.process_utils import check_call_collect


@register_endpoint(
    description="Print version",
)
def version() -> None:
    print(VERSION_STR)


@register_endpoint(
    configs=[ConfigData],
    description="Install a package from the local folder",
)
def install_from_local() -> None:
    dist_folder = "dist"

    if os.path.isdir(dist_folder):
        shutil.rmtree(dist_folder)
    args = [
        ConfigData.python,
        "setup.py",
        "sdist",
    ]
    if ConfigData.setup_quiet:
        args.extend(["--quiet"])
    check_call_collect(args)
    files = list(os.listdir(dist_folder))
    assert len(files) == 1, f"too many files in {dist_folder}"
    new_file = os.path.join(dist_folder, files[0])
    args = []
    if ConfigData.use_sudo:
        args.extend(["sudo", "-H"])
    args.extend(
        [ConfigData.pip, "install", "--quiet", "--upgrade", new_file]
    )
    if ConfigData.pip_quiet:
        args.extend(["--quiet"])
    if ConfigData.install_in_user_folder:
        args.extend(["--user"])
    check_call_collect(args)


@register_endpoint(
    configs=[ConfigData],
    description="Install a package from pypi or gemfury",
)
def install_from_remote() -> None:
    args = []
    if ConfigData.use_sudo:
        args.extend(["sudo", "-H"])
    args.extend(
        [
            ConfigData.pip,
            "install",
            "--upgrade",
            f"{ConfigData.module_name}",
        ]
    )
    if ConfigData.pip_quiet:
        args.extend(["--quiet"])
    if ConfigData.install_in_user_folder:
        args.extend(["--user"])
    pypitools.process_utils.check_call_collect(args)
    output = subprocess.check_output(
        [
            ConfigData.pip,
            "show",
            f"{ConfigData.module_name}",
        ]
    ).decode()
    for line in output.split("\n"):
        if line.startswith("Version"):
            print(line)


@register_endpoint(
    configs=[ConfigData],
    description="Upload a package to pypi or gemfury",
)
def upload() -> None:
    """
    This script uploads your module to where ever you configure it.
    It's default is to upload to pypi but you can override by putting
    a pypi.cnf file in the root of your source tree.

    It does the following:
    - clean
    - setup.py sdist
    - twine upload
    - clean again

    Notes:
    - This script could be done via setuptools using the following:
    $ python3 setup.py sdist upload -r pypi --identity="Mark Veltzer" --sign
    but this has bad security implications as it sends user and password plain text.
    - we use twine(1) to upload the package.
    On ubuntu twine(1) is from the 'twine' official ubuntu package.

    References:
    - https://pypi.python.org/pypi/twine
    - https://python-packaging-user-guide.readthedocs.org/en/latest/index.html
    - http://peterdowns.com/posts/first-time-with-pypi.html
    """
    clean_before_if_needed()
    package_it()
    check_if_needed()
    try:
        upload_select()
    finally:
        clean_after_if_needed()


@register_endpoint(
    configs=[ConfigData],
    description="Register a function on pypi or gemfury",
)
def register() -> None:
    """
    This function registers your project in pypi.

    when registering via twine(1) you need to:
    - full clean
    - build wheel using setup.py
    - twine register
    - full clean
    This method works, if you register twice it is ok.
    You just need to do it once...:)

    when registering via setup.py you need to:
    - full clean
    - python setup.py register -r pypi
    - full clean
    registering the same package many times works.
    You just need to do it once...:)

    References:
    - https://packaging.python.org/distributing/

    TODO:
    - check if I'm already registered and don't register if that is the case.
    """
    clean_before_if_needed()
    package_it()
    check_if_needed()
    try:
        register_select()
    finally:
        clean_after_if_needed()


@register_endpoint(
    configs=[ConfigData],
    description="Package in source and/or wheel format",
)
def package() -> None:
    package_it()


@register_endpoint(
    configs=[ConfigData],
    description="Package and check if the package is correct",
)
def check() -> None:
    package_it()
    check_if_needed()


@register_endpoint(
    configs=[ConfigData],
    description="Upgrade to new version",
)
def bump() -> None:
    """
    This will:
    - check that all is committed
    - bump the version
    - run pydmt build
    - commit with a standard message
    - tag with a standard message
    - push
    - upload to pypi
    """
    # check_all_is_committed()
    check_if_needed()


@register_endpoint(
    configs=[ConfigData],
    description="Get all pre requisites into a folder",
)
def prerequisites() -> None:
    do_prerequisites()


@register_endpoint(
    configs=[ConfigData],
    description="Get run pre requisites into a folder",
)
def prerequisites_run() -> None:
    import config.python
    do_prerequisites(config.python.run_requires)


@register_main(main_description=DESCRIPTION)
def main():
    pylogconf.core.setup()
    config_arg_parse_and_launch()


if __name__ == "__main__":
    main()
