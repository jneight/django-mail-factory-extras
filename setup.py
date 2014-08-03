# coding=utf-8

import os
from setuptools import setup, find_packages
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

import mailfactory_extras as me

setup(
    name='django-mailfactory-extras',
    version=me.__version__,
    url='https://github.com/jneight/django-mailfactory-extras',
    install_requires=['django-mail-factory'],
    description="Extensions for django-mail-factory, like django-xadmin integration or asynchronous message sending",
    author=me.__author__,
    author_email=me.__email__,
    packages=find_packages(exclude=['tests', 'tests.*',]),
    include_package_data=True,
    license=me.__license__,
    test_suite="tests",
)
