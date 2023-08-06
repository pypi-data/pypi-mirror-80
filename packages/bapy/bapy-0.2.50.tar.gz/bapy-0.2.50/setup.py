#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The setup script."""
from setuptools import setup, find_packages

import bapy

author, author_email, name, description, install_requires, scripts, setup_requires, tests_require, url = bapy.setup()

setup(
    author=author,
    author_email=author_email,
    description=description,
    entry_points={
        'console_scripts': [
            f'{name} = {name}:app',
        ],
    },
    include_package_data=True,
    install_requires=install_requires,
    name=name,
    package_data={
        name: [f'{name}/scripts/*', f'{name}/templates/*'],
    },
    packages=find_packages(),
    python_requires='>=3.8,<4',
    scripts=scripts,
    setup_requires=setup_requires,
    tests_require=tests_require,
    url=url,
    use_scm_version=False,
    version='0.2.50',
    zip_safe=False,
)
