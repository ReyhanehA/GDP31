#!/usr/bin/env python
# -*- coding: utf-8 -*-
import easyxlsx
from setuptools import setup, find_packages

install_requires = ['XlsxWriter>=0.7.3']

setup(
    name='easyXlsx',
    version=easyxlsx.__version__,
    description='excel export component.',
    author='tommao',
    author_email='istommao@gmail.com',
    install_requires=install_requires,
    packages=find_packages('easyxlsx'),
    package_dir={'': 'easyxlsx'},   # 告诉distutils包都在easyxlsx下
    license='MIT',
    url='https://github.com/istommao/easyXlsx'
)
