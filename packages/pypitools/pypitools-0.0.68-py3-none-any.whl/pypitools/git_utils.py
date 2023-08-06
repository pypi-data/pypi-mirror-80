from pypitools.process_utils import check_call_collect


def git_clean_full() -> None:
    """
    Clean the current git repo in a strict way
    """
    check_call_collect(["git", "clean", "-qffxd"])
