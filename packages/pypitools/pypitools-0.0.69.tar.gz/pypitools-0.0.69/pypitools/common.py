"""
This is common pypitools functionality
"""
import os
import shutil
import sys
from typing import List

from pypitools.configs import UploadMethod, RegisterMethod, ConfigData
from pypitools.git_utils import git_clean_full
from pypitools.name_utils import get_package_filename, get_package_wheelname
from pypitools.process_utils import check_call_collect


def check_by_twine() -> None:
    """
    check by twine
    """
    args = [
        "twine",
        "check",
    ]
    to_check = 0
    if ConfigData.upload_sdist:
        args.append(get_package_filename())
        to_check += 1
    if ConfigData.upload_wheel:
        args.append(get_package_wheelname())
        to_check += 1
    (out, err) = check_call_collect(args)
    out_lines = out.rstrip().split("\n")
    if len(out_lines) > to_check:
        print(out, end="", file=sys.stdout)
        print(err, end="", file=sys.stderr)
        sys.exit(1)


def check_if_needed() -> None:
    if ConfigData.check_before_upload:
        check_by_twine()


def upload_by_setup() -> None:
    """
    upload by setup.py sdist upload

    This method still works although it is legacy
    
    see: python setup.py upload --help
    """
    args = [
        ConfigData.python,
        "setup.py",
    ]
    if ConfigData.upload_sdist:
        args.append("sdist")
    if ConfigData.upload_wheel:
        args.append("bdist_wheel")
    args.extend(
        [
            "upload",
            # this means which repository to upload too
            # the default is https://upload.pypi.org/legacy/ and it works
            # '-r',
            # 'pypi',
        ]
    )
    check_call_collect(args)


def upload_by_twine() -> None:
    """
    upload by twine
    """
    package_it()
    if ConfigData.check_before_upload:
        check_by_twine()
    args = [
        "twine",
        "upload",
    ]
    if ConfigData.upload_sdist:
        args.append(get_package_filename())
    if ConfigData.upload_wheel:
        args.append(get_package_wheelname())
    check_call_collect(args)


def upload_by_gemfury() -> None:
    """
    upload to gemfury

    The command line is the one recommended by gemfury at
    https://manage.fury.io/dashboard/[username]/push
    """
    package_it()
    if ConfigData.check_before_upload:
        check_by_twine()
    check_call_collect(
        [
            "fury",
            "push",
            get_package_filename(),
            f"--as={ConfigData.gemfury_user}",
        ]
    )


def upload_select() -> None:
    """
    upload via the method configured
    """
    if ConfigData.upload_method == UploadMethod.SETUP:
        upload_by_setup()
    if ConfigData.upload_method == UploadMethod.TWINE:
        upload_by_twine()
    if ConfigData.upload_method == UploadMethod.GEMFURY:
        upload_by_gemfury()


def register_by_setup() -> None:
    """
    register via setup.py register
    """
    check_call_collect(
        [ConfigData.python, "setup.py", "register", "-r", "pypi"]
    )


def register_by_twine() -> None:
    """
    register via the twine method
    """
    check_call_collect(["twine", "register", get_package_filename()])


def register_select() -> None:
    """
    Register via the method configured
    """
    if ConfigData.register_method == RegisterMethod.TWINE:
        register_by_twine()
    if ConfigData.register_method == RegisterMethod.SETUP:
        register_by_setup()
    if ConfigData.register_method == RegisterMethod.UPLOAD:
        upload_select()


def clean_before_if_needed() -> None:
    """
    Clean the git repo if needed
    """
    if ConfigData.clean_before:
        git_clean_full()


def clean_after_if_needed() -> None:
    """
    Clean the git repo if needed
    """
    if ConfigData.clean_after:
        git_clean_full()


def package_it() -> None:
    """
    package our module
    """
    args = [
        ConfigData.python,
        "setup.py",
    ]
    if ConfigData.upload_sdist:
        args.append("sdist")
    if ConfigData.upload_wheel:
        args.append("bdist_wheel")
    check_call_collect(args)


def do_prerequisites(packages: List[str] = None) -> None:
    """
    Gather all prerequisites into a single folder
    """
    if os.path.exists(ConfigData.wheel_folder):
        shutil.rmtree(ConfigData.wheel_folder)
    os.mkdir(ConfigData.wheel_folder)
    args = [
        ConfigData.pip,
        "wheel",
        "--wheel-dir",
        ConfigData.wheel_folder,
    ]
    if packages is None:
        args.extend([
            "--requirement",
            ConfigData.requirements,
        ])
    else:
        args.extend(packages)
    check_call_collect(args)
