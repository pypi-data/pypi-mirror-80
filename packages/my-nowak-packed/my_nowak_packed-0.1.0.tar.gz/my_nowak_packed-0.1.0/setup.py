#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name='my_nowak_packed',
    version='0.1.0',
    author='SomeCompoany PLC',
    author_email='dev@onet.pl',
    packages=find_packages(),
    include_package_data=True,
    keywords='random names',
    description='Super library very interested',
    install_requires=['names']


)