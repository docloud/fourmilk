#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='fourmilk',
    version='1.0.0',
    description='fourmilk Project',
    url='http://github.com/docloud/fourmilk',
    include_package_data=True,
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            'fourmilk=fourmilk.shell:cli'
        ]
    },
    install_requires=open('requirements.txt').readlines(),
)
