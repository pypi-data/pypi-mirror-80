from dataclasses import dataclass
from typing import Optional, List
import sys
import os
import subprocess
from zuper_commons.types import ZException
from .import logger
import traceback
__all__ = ['aido_dir_status_main', 'DirInfo', 'get_dir_info']


@dataclass
class DirInfo:
    tag: Optional[str]
    """ Tag for this """
    dirty: bool
    added: List[str]
    modified: List[str]
    untracked: List[str]

def get_status(dirname: str):
    cmd = ["git", "status", "--porcelain"]
    res = subprocess.run(cmd, cwd=dirname, capture_output=True)
    if res.returncode:
        sys.exit(-3)
    stdout = res.stdout.decode()
    lines = stdout.split('\n')

    modified = []
    added = []
    untracked  = []
    for l in lines:
        l = l.strip()
        if not l: continue
        status, _, filename = l.partition(' ')
        # logger.info(status=status, filename=filename)
        if status == '??':
            untracked.append(filename)
        elif status == 'M':
            modified.append(filename)
        elif status in ['A', 'AM']:
            added.append(filename)
        else:
            raise ZException(stdout=stdout)
    return modified, added, untracked

def get_tag(dirname) -> Optional[str]:
    cmd = ["git", "describe", "--exact-match", "--tags"]
    res = subprocess.run(cmd, cwd=dirname, stdout=subprocess.PIPE)
    tagged = res.returncode == 0
    if tagged:
        tag = res.stdout.decode()
    else:
        tag = None
    return tag

def get_dir_info(dirname: str) -> DirInfo:
    if not os.path.exists(dirname):
        sys.exit(-2)

    tag = get_tag(dirname)

    modified, added, untracked = get_status(dirname)


    dirty = bool(modified or added or untracked)
    di = DirInfo(tag=tag, dirty=dirty, modified=modified, added=added, untracked=untracked)
    return di





def aido_dir_status_main():
    try:
        res = get_dir_info('.')
        logger.info(res=res)
    except SystemExit:
        raise
    except BaseException as e:
        logger.error(traceback.format_exc())
        sys.exit(3)

if __name__ == '__main__':
    auto_dir_status_main()
