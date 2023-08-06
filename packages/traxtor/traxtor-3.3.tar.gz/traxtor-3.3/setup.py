#!/usr/bin/python3
#2020 Danial Behzadi
#Released under GPLv3+

import re
import setuptools


with open("README.md", "r") as readme:
    long_description = readme.read()

with open("debian/changelog", "r") as changelog:
    latest = changelog.readline()
version = re.split('\(|\)', latest)[1]

with open("debian/control", "r") as control:
    for line in control:
        if line.startswith("Maintainer: "):
            maintainer = re.split(': | <|>', line)
        elif line.startswith("Description: "):
            description = re.split(': |\n', line)[1]
        #elif line.startswith("Package: "):
        #    name = line.split()[1]


setuptools.setup(
    name='traxtor',
    version=version,
    author=maintainer[1],
    author_email=maintainer[2],
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/tractor-team/tractor",
    packages=setuptools.find_packages(),
    package_data={
        'tractor': ['SampleBridges', 'tractor.gschema.xml']
    },
    project_urls={
        "Bug Tracker": "https://gitlab.com/tractor-team/tractor/-/issues",
        "Documentation": "https://gitlab.com/tractor-team/tractor/-/blob/master/man/tractor.1",
        "Source Code": "https://gitlab.com/tractor-team/tractor",
    },
    install_requires=[
        'PyGObject',
        'fire',
        'psutil',
        'requests',
        'stem',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        "console_scripts": [
            "tractor = tractor.tractor:main",
        ],
    }
)
