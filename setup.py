# -*- coding: utf-8 -*-
from setuptools import setup


setup(
    name='dj-queryset-manager',
    version='0.1.0-alpha',
    url='https://github.com/nosamanuel/dj-queryset-manager',
    license=open('LICENSE').read(),
    author='Noah Seger',
    author_email='nosamanuel@gmail.com.com',
    description='Stop writing Django querysets.',
    long_description=open('README.rst').read(),
    py_modules=['dj_queryset_manager'],
    test_suite='tests',
    tests_require=['Django>=1.2']
)
