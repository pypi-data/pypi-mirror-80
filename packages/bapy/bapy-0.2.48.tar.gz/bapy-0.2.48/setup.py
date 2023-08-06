#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The setup script."""
from setuptools import setup, find_packages

import bapy

bapy.ic(bapy.path)
setup(
    author=bapy.User.gecos,
    author_email=bapy.Url.email(),
    description=bapy.path.project.description(),
    entry_points={
        'console_scripts': [
            f'{bapy.path.repo} = {bapy.path.repo}:app',
        ],
    },
    include_package_data=True,
    install_requires=bapy.path.project.requirements['requirements'],
    name=bapy.path.repo,
    package_data={
        bapy.path.repo: [f'{bapy.path.repo}/scripts/*', f'{bapy.path.repo}/templates/*'],
    },
    packages=find_packages(),
    python_requires='>=3.8,<4',
    scripts=bapy.path.scripts_relative,
    setup_requires=bapy.path.project.requirements['requirements_setup'],
    tests_require=bapy.path.project.requirements['requirements_test'],
    url=bapy.Url.lumenbiomics(http=True, repo=bapy.path.repo).url,
    use_scm_version=False,
    version='0.2.48',
    zip_safe=False,
)
