#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


# This command has been borrowed from
# https://github.com/getsentry/sentry/blob/master/setup.py
class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ["tests"]
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.test_args)
        sys.exit(errno)


def read(f):
    return open(f, "r", encoding="utf-8").read()


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, "__init__.py")).read()
    return re.search(
        "^__version__ = ['\"]([^'\"]+)['\"]", init_py, re.MULTILINE
    ).group(1)


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [
        dirpath
        for dirpath, dirnames, filenames in os.walk(package)
        if os.path.exists(os.path.join(dirpath, "__init__.py"))
    ]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [
        (dirpath.replace(package + os.sep, "", 1), filenames)
        for dirpath, dirnames, filenames in os.walk(package)
        if not os.path.exists(os.path.join(dirpath, "__init__.py"))
    ]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend(
            [os.path.join(base, filename) for filename in filenames]
        )
    return {package: filepaths}


name = "djangorestframework-xml"
package = "rest_framework_xml"
version = get_version(package)
description = "XML support for Django REST Framework"
url = "https://github.com/jpadilla/django-rest-framework-xml"
author = "José Padilla"
author_email = "hello@jpadilla.com"
license = "BSD"
install_requires = ["defusedxml>=0.6.0"]
extras_requires = {
    "docs": ["mkdocs>=0.11.1"],
    "tests": [
        "Django>=1.6",
        "djangorestframework>=2.4.3",
        "pytest-django",
        "pytest",
        "flake8",
    ],
}

extras_requires["dev"] = (
    extras_requires["docs"] + extras_requires["tests"] + ["tox", "pre-commit"]
)


if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    os.system("python setup.py bdist_wheel upload")
    print("You probably want to also tag the version now:")
    print("  git tag -a {0} -m 'version {0}'".format(version))
    print("  git push --tags")
    sys.exit()

setup(
    name=name,
    version=version,
    url=url,
    license=license,
    description=description,
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author=author,
    author_email=author_email,
    packages=get_packages(package),
    package_data=get_package_data(package),
    cmdclass={"test": PyTest},
    install_requires=install_requires,
    extras_require=extras_requires,
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP",
    ],
)
