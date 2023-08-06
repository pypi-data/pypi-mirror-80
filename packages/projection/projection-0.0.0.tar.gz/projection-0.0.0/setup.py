#!/usr/bin/env python

"""
Setuptools configuration
"""

import sys

from pathlib import Path  # noqa
from setuptools import setup, find_packages  # noqa

sys.path.insert(0, "src")

from projection import __version__ as version_string  # noqa


#
# Options
#

name = "projection"

description = "Project Configuration"

readme_path = Path(__file__).parent / "README.rst"
try:
    long_description = readme_path.open().read()
except IOError:
    long_description = None

url = "https://github.com/wsanchez/projection"

author = "Wilfredo Sánchez Vega"

author_email = "wsanchez@wsanchez.net"

license = "Apache License, Version 2.0"

platforms = ["all"]

packages = find_packages(where="src")

classifiers = [
    "Framework :: Twisted",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
]


#
# Entry points
#

entry_points = dict(console_scripts=["project = project.run:Command.main"])


#
# Package data
#

package_data = dict(projection=[])


#
# Dependencies
#

python_requirements = ">=3.6"

setup_requirements = []

install_requirements = [
    # Direct dependencies
    "attrs==19.3.0",
    "Twisted==20.3.0",

    # Indirect dependencies
]

extras_requirements = {}


#
# Set up Extension modules that need to be built
#

extensions = []


#
# Run setup
#

def main():
    """
    Run :func:`setup`.
    """
    setup(
        name=name,
        version=version_string,
        description=description,
        long_description=long_description,
        long_description_content_type="text/x-rst",
        url=url,
        classifiers=classifiers,
        author=author,
        author_email=author_email,
        license=license,
        platforms=platforms,
        packages=packages,
        package_dir={"": "src"},
        package_data=package_data,
        entry_points=entry_points,
        data_files=[],
        ext_modules=extensions,
        python_requires=python_requirements,
        setup_requires=setup_requirements,
        install_requires=install_requirements,
        extras_require=extras_requirements,
    )


#
# Main
#

if __name__ == "__main__":
    main()
