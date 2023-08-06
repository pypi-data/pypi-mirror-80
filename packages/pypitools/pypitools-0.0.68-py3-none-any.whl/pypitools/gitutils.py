from pypitools.process_utils import check_call_no_output


def git_clean_full() -> None:
    """
    Clean the current git repo in a strict way
    """
    check_call_no_output(["git", "clean", "-qffxd"])
