#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as file:
    long_description = file.read()

with open('requirements.txt') as file:
    requirements = file.read()

setup(
    name='imagine',
    version='0.1.0',
    url='https://github.com/waawal/imagine',
    license='MIT',
    author='Daniel Waardal',
    author_email='waawal@boom.ws',
    description='Do stuff with images!',
    long_description=long_description,
    py_modules=['imagine'],
    zip_safe=True,
    platforms='any',
    install_requires=requirements,
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)