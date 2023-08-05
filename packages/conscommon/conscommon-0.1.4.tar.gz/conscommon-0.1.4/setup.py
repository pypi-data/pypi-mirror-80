#!/usr/bin/env python
from setuptools import setup, find_namespace_packages
from conscommon import __version__, __author__

import pkg_resources


def get_abs_path(relative):
    return pkg_resources.resource_filename(__name__, relative)


with open(get_abs_path("README.md"), "r") as _f:
    long_description = _f.read().strip()

with open(get_abs_path("requirements.txt"), "r") as _f:
    requirements = _f.readlines()

setup(
    author=__author__,
    classifiers=[
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
        "Operating System :: OS Independent",
    ],
    description="Commons for Sirius applications",
    download_url="https://github.com/lnls-sirius/cons-common",
    include_package_data=True,
    install_requires=requirements,
    license="GNU GPLv3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="conscommon",
    packages=find_namespace_packages(include=["conscommon", "conscommon.*"]),
    python_requires=">=3.6",
    url="https://github.com/lnls-sirius/cons-common/",
    version=__version__,
)
