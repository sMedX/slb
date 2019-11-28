# -*- coding: utf-8 -*-
"""
Project setup module
"""
import os
import os.path
from typing import List

from setuptools import find_packages
from setuptools import setup

name = 'slb_task2-backend'
version = '0.1.0'


def find_requires() -> List[str]:
    """
    find project package requirements

    :return: List of project package requirements
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    reqs_path = os.path.join(dir_path, "requirements.txt")

    with open(reqs_path, 'r') as reqs:
        requirements = reqs.readlines()
    return requirements


if __name__ == "__main__":
    setup(
        name=name,
        version=version,
        description='slb_task2 Backend implementation',
        long_description="""slb_task2 Backend implementation""",
        classifiers=[
            "Development Status :: 4 - Beta",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
        ],
        packages=find_packages(),
        install_requires=find_requires(),
        include_package_data=True,
        entry_points={
            'console_scripts': [
                'slb_task2 = slb_task2.cli:main',
            ],
        },
    )
