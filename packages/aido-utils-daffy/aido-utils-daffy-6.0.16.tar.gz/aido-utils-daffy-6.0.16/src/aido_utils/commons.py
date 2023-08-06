import argparse
import subprocess
import sys
import traceback
from dataclasses import dataclass
from typing import List, Optional, Tuple

from zuper_commons.types import ZException

from . import logger

__all__ = ["aido_dir_status_main", "DirInfo", "get_dir_info"]


@dataclass
class DirInfo:
    tag: Optional[str]
    """ Tag for the commit """
    branch: str
    dirty: bool
    added: List[str]
    modified: List[str]
    deleted: List[str]
    untracked: List[str]
    closest_tag: Optional[str]
    repo_name: str
    sha: str
    vcs_url: str


def get_dir_info(dirname: str) -> DirInfo:
    tag = get_tag(dirname)

    modified, added, deleted, untracked = get_status(dirname)
    sha = get_sha(dirname)
    closest_tag = get_closest_tag(dirname)
    vcs_url, repo_name = get_origin_url_repo(dirname)
    branch = get_branch(dirname)

    dirty = bool(modified or added or deleted or untracked)
    if dirty:
        sha += "-dirty"
    di = DirInfo(
        tag=tag,
        dirty=dirty,
        modified=modified,
        added=added,
        deleted=deleted,
        untracked=untracked,
        vcs_url=vcs_url,
        closest_tag=closest_tag,
        repo_name=repo_name,
        sha=sha,
        branch=branch,
    )
    return di


def get_sha(dirname: str) -> str:
    sha = _run_cmd(["git", "-C", dirname, "rev-parse", "HEAD"])[0]
    return sha


def get_branch(dirname: str) -> str:
    branch = _run_cmd(["git", "-C", dirname, "rev-parse", "--abbrev-ref", "HEAD"])[0]
    return branch


def get_head_tag(dirname: str) -> Optional[str]:
    head_tag = _run_cmd(["git", "-C", dirname, "describe", "--exact-match", "--tags", "HEAD",])

    head_tag = head_tag[0] if head_tag else None
    return head_tag


def get_closest_tag(dirname: str) -> Optional[str]:
    closest_tag = _run_cmd(["git", "-C", dirname, "tag"])
    closest_tag = closest_tag[-1] if closest_tag else None
    return closest_tag


def get_origin_url_repo(dirname: str) -> Tuple[str, str]:
    origin_url0 = _run_cmd(["git", "-C", dirname, "config", "--get", "remote.origin.url"])[0]
    origin_url = origin_url0
    if origin_url.endswith(".git"):
        origin_url = origin_url[:-4]
    if origin_url.endswith("/"):
        origin_url = origin_url[:-1]
    repo = origin_url.split("/")[-1]
    return origin_url0, repo


def _run_cmd(cmd: List[str]) -> List[str]:
    # logger.debug(cmd)
    output = subprocess.check_output(cmd)

    lines = output.decode("utf-8").split("\n")

    return [line.strip() for line in lines if line.strip()]


def get_status(dirname: str):
    cmd = ["git", "status", "--porcelain"]
    res = subprocess.run(cmd, cwd=dirname, capture_output=True)
    if res.returncode:
        sys.exit(-3)
    stdout = res.stdout.decode()
    lines = stdout.split("\n")

    modified = []
    added = []
    untracked = []
    deleted = []

    IGNORE = ["Makefile", ".gitignore"]
    for l in lines:
        l = l.strip()
        if not l:
            continue
        status, _, filename = l.partition(" ")

        if filename in IGNORE:
            continue

        # logger.info(status=status, filename=filename)
        if status == "??":
            untracked.append(filename)
        elif status == "M":
            modified.append(filename)
        elif status in ["A", "AM"]:
            added.append(filename)
        elif status in ["D"]:
            deleted.append(filename)
        else:
            raise ZException(stdout=stdout)
    return modified, added, deleted, untracked


def get_tag(dirname) -> Optional[str]:
    cmd = ["git", "describe", "--exact-match", "--tags"]
    res = subprocess.run(cmd, cwd=dirname, stdout=subprocess.PIPE)
    tagged = res.returncode == 0
    if tagged:
        tag = res.stdout.decode().strip()
    else:
        tag = None
    return tag


def aido_dir_status_main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", "-d", default=".")
    parsed = parser.parse_args(args)
    dirname = parsed.directory
    try:
        res = get_dir_info(dirname)
        logger.info(res=res)
    except SystemExit:
        raise
    except BaseException as e:
        logger.error(traceback.format_exc())
        sys.exit(3)
