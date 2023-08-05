#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The setup script."""
from setuptools import setup, find_packages

from bapy import path, Url, User

setup(
    author=User.gecos,
    author_email=Url.email(User.name),
    description=path.project.description(),
    entry_points={
        'console_scripts': [
            f'{path.repo} = {path.repo}:app',
        ],
    },
    include_package_data=True,
    install_requires=path.project.requirements['requirements'],
    name=path.repo,
    package_data={
        path.repo: [f'{path.repo}/scripts/*', f'{path.repo}/templates/*'],
    },
    packages=find_packages(include=[path.repo], exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    python_requires='>=3.8,<4',
    scripts=path.scripts,
    setup_requires=path.project.requirements['requirements_setup'],
    tests_require=path.project.requirements['requirements_test'],
    url=Url.lumenbiomics(http=True, repo=path.repo).url,
    use_scm_version=False,
    version='0.1.65',
    zip_safe=False,
)
