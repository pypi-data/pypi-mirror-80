from setuptools import setup


def get_version(filename: str):
    import ast

    version = None
    with open(filename) as f:
        for line in f:
            if line.startswith("__version__"):
                version = ast.parse(line).body[0].value.s
                break
        else:
            raise ValueError("No version found in %r." % filename)
    if version is None:
        raise ValueError(filename)
    return version


version = get_version(filename="src/aido_utils/__init__.py")

install_requires = (["requirements-parser", "zuper-commons-z6", "packaging", "pytz", "whichcraft"],)

line = "daffy"

setup(
    name=f"aido-utils-{line}",
    version=version,
    keywords="",
    package_dir={"": "src"},
    packages=["aido_utils"],
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "aido-update-reqs=aido_utils.update_req_versions:update_reqs_versions_main",
            "aido-dir-status=aido_utils:aido_dir_status_main",
            "aido-check-tagged=aido_utils:aido_check_tagged_main",
            "aido-check-not-dirty=aido_utils:aido_check_not_dirty_main",
            "aido-check-need-upload=aido_utils:aido_check_need_upload_main",
            "aido-labels=aido_utils:aido_labels_main",
        ],
    },
)
