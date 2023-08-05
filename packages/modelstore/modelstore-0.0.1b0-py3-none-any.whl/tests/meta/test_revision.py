import os
import subprocess

import git

from modelstore.meta import revision

# pylint: disable=protected-access


def test_repo_name():
    repo = git.Repo(search_parent_directories=True)
    assert revision._repo_name(repo) == "operator.ai"


def test_fail_gracefully():
    # Assumes that there is no git repo at /
    current_wd = os.getcwd()
    os.chdir("/")
    assert revision.git_meta() is None
    os.chdir(current_wd)


def test_git_meta():
    res = subprocess.check_output("git log . | head -n 1", shell=True)
    exp = res.decode("utf-8").strip().split(" ")[1]
    meta = revision.git_meta()

    assert meta is not None
    assert meta["repository"] == "operator.ai"
    if meta["local_changes"] is False:
        assert meta["sha"] == exp
