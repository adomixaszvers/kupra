#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='KuPRA',
    version='1.0',
    description='OpenShift App',
    author='Adomas Jatužis',
    author_email='adomixaszvers@gmail.com',
    url='http://www.python.org/sigs/distutils-sig/',
    install_requires=['Django',
        'django-user-accounts',
        'pinax-theme-bootstrap',
        'django-debug-toolbar',
        'django-suit',],
)
