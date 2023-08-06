#!/usr/bin/env python

import re
from os.path import abspath, dirname, join
from setuptools import setup


CURDIR = dirname(abspath(__file__))

CLASSIFIERS = '''
Development Status :: 5 - Production/Stable
License :: OSI Approved :: Apache Software License
Operating System :: OS Independent
Programming Language :: Python :: 3
Topic :: Software Development :: Testing
Framework :: Robot Framework :: Library
'''.strip().splitlines()
with open(join(CURDIR, 'version.py'), encoding="utf-8") as f:
    VERSION = re.search("__version__ = '(.*)'", f.read()).group(1)
with open(join(CURDIR, 'requirements.txt')) as f:
    REQUIREMENTS = f.read().splitlines()

setup(
    name='da-rover',
    version=VERSION,
    description="Custom Integration Bridge between tools like CA ARD, HP QC/ALM and ALM Octane",
    author="Rakesh Ummadisetty",
    author_email='u.rakesh@live.com',
    url='https://github.com/raka2407/octane-transformer.git',
    license          = 'MIT',
    keywords         = 'ard alm qc octane',
    platforms        = 'any',
    install_requires = REQUIREMENTS,  
    classifiers=CLASSIFIERS,
    packages=['da_rover'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'rover=da_rover.runner:main',
        ]
    }
)
