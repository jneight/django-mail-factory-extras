# coding=utf-8


from setuptools import setup, find_packages

import mailfactory_extras as me

setup(
    name='django-mailfactory-extras',
    version=me.__version__,
    url='https://github.com/jneight/django-mailfactory-extras',
    install_requires=['django-mail-factory'],
    description="Extensions for django-mail-factory, like django-xadmin integration or asynchronous message sending",
    author=me.__author__,
    author_email=me.__email__,
    include_package_data=True,
    packages=find_packages(),
    license=me.__license__,
    test_suite="tests",
)
