#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Setup and install the pacifica service."""
from os import path
from setuptools import setup, find_packages


setup(
    name='pacifica-auth',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    description='Pacifica Authentication Library',
    url='https://github.com/pacifica/pacifica-auth/',
    long_description=open(path.join(
        path.abspath(path.dirname(__file__)),
        'README.md')).read(),
    long_description_content_type='text/markdown',
    author='David Brown',
    author_email='dmlb2000@gmail.com',
    packages=find_packages(exclude='tests'),
    namespace_packages=['pacifica'],
    install_requires=[
        'cherrypy',
        'sqlalchemy',
        'social-auth-core',
        'social-auth-app-cherrypy',
        'jinja2',
    ]
)
