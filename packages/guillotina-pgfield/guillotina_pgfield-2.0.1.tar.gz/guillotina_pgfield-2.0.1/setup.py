# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

import re


def load_reqs(filename):
    with open(filename) as reqs_file:
        return [
            re.sub("==", ">=", line)
            for line in reqs_file.readlines()
            if not (re.match("\s*#", line) or re.match("-e", line))
        ]


requirements = load_reqs("requirements.txt")
test_requirements = load_reqs("requirements-test.txt")

setup(
    name="guillotina_pgfield",
    version=open("VERSION").read().strip(),
    description="Postgres field support for Guillotina",
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    url="https://flaps.io",
    license="BSD",
    setup_requires=["pytest-runner"],
    zip_safe=True,
    include_package_data=True,
    packages=find_packages(),
    install_requires=requirements,
    tests_require=test_requirements,
)
