#!/usr/bin/env python

from distutils.core import setup
from os.path import abspath, dirname, join
import re
from setuptools import setup, find_packages

NAME = 'rpbot'
CLASSIFIERS = """
Development Status :: 4 - Beta
Operating System :: OS Independent
Programming Language :: Python
Topic :: Software Development :: Testing
""".strip().splitlines()
CURDIR = dirname(abspath(__file__))
with open(join(CURDIR, 'rpbot', '__init__.py')) as f:
    VERSION = re.search("\n__version__ = '(.*)'\n", f.read()).group(1)
with open(join(CURDIR, 'README.md')) as f:
    README = f.read()
CURDIR = dirname(abspath(__file__))
with open(join(CURDIR, 'requirements.txt')) as f:
    REQUIREMENTS = f.read().splitlines()
    REQUIREMENTS = [r.split('#egg=')[-1] for r in REQUIREMENTS]

setup(
    name             = NAME,
    version          = VERSION,
    author           = 'Doyou Jung',
    author_email     = 'doyou89@gmail.com',
    url              = 'https://github.com/doyou89/RPBot',
    download_url     = 'https://pypi.python.org/pypi/rpbot',
    license          = 'Apache License 2.0',
    description      = 'A tool for inserting Robot Framework test run results into ReportPortal.',
    long_description = README,
    long_description_content_type = 'text/markdown',
    keywords         = 'robotframework testing testautomation atdd',
    platforms        = 'any',
    classifiers      = CLASSIFIERS,
    packages         = find_packages(),
    install_requires = REQUIREMENTS,
)
