from six.moves import urllib
from . import logger
from typing import Dict, Optional
import argparse
from zuper_commons.types import ZException, ZKeyError
import traceback
from whichcraft import which
import subprocess
import json
import sys
from .commons import get_dir_info
import requests

import os

__all__ = ['aido_check_need_upload_main']


def download_json(url: str, headers: Dict[str, str] = None):
    headers = headers or {}

    r = requests.get(url, headers=headers)
    logger.info(url=url)

    if r.status_code == 404:
        logger.info(f'404 {url}')
        raise ZKeyError(url=url, r=r)
    else:
        j = json.dumps(r.json())
        return j


def interpret_pypi(json_string):
    rj = json.loads(json_string)
    pypi_version = rj["info"]["version"]
    return pypi_version


def interpret_devpi(json_string):
    rj = json.loads(json_string)

    # logger.info(rj=rj )
    versions = list(rj["result"])

    version_sorted = sorted(versions, key=lambda _: tuple(map(int, _.split('.'))))

    v = version_sorted[-1]

    logger.info(v=v, version_sorted=version_sorted)

    return v


def get_pip_server():
    default = 'https://pypi.org/pypi'
    r = os.environ.get('PIP_INDEX_URL', default)
    if r.endswith('/'):
        r = r[:-1]
    return r


class CouldNotGetVersion(ZException):
    pass


def get_last_version_fresh(package_name) -> Optional[str]:
    pip_server = get_pip_server()
    logger.info(pip_server=pip_server)
    if 'pypi.org' in pip_server:
        url = f"{pip_server}/{package_name}/json"
        headers = {"Accept": "application/json"}
        try:
            json = download_json(url, headers=headers)
        except ZKeyError:
            return None
        return interpret_pypi(json)
    else:
        headers = {"Accept": "application/json"}
        url = f"{pip_server}/{package_name}"
        try:
            json = download_json(url, headers=headers)
        except ZKeyError:
            return None

        return interpret_devpi(json)


def aido_check_need_upload_main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', '-d', default=".")
    parser.add_argument('--package')
    parser.add_argument('cmd', nargs='*')
    parsed = parser.parse_args(args)
    if parsed.package is None:
        raise ZValueError('--package')
    package = parsed.package

    try:
        directory = parsed.directory
        absdir = os.path.realpath(directory)
        rest = parsed.cmd

        if not os.path.exists(directory):
            sys.exit(-2)

        di = get_dir_info(directory)

        if di.tag is None:
            logger.error('This is not tagged. ',
                         directory=absdir, di=di, rest=" ".join(rest))
            sys.exit(1)

        else:
            try:
                last_version = get_last_version_fresh(package)
            except BaseException as e:
                logger.error(traceback.format_exc())
                last_version = 'n/a'
            # logger.info('This is tagged. ',
            #             directory=absdir, di=di, last_version=last_version)

            tag1 = f'v{last_version}'
            if tag1 == di.tag:
                logger.info(f'Already present version {last_version}', absdir=absdir, package=package)
                sys.exit(0)
            else:
                logger.info(f'Tag {di.tag!r} but version {last_version!r} tag1 = {tag1!r}',
                            absdir=absdir, package=package)
                res = subprocess.run(rest, cwd=directory)
                sys.exit(res.returncode)

    except SystemExit:
        raise
    except BaseException as e:
        logger.error(traceback.format_exc())
        sys.exit(3)
