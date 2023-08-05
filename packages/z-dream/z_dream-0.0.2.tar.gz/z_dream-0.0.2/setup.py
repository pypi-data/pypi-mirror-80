#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='z_dream',
    version='0.0.2',
    author='Z-Dream',
    author_email='z_dream@126.com',
    url='http://misso.tech/',
    description='test',
    packages=['z_dream'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'dream1=z_dream:test1',
            'dream2=z_dream:test2'
        ]
    }
)