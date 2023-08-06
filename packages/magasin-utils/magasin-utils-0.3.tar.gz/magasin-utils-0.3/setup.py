#!/usr/bin/env python
import ast
import os.path
import re
from codecs import open

from setuptools import setup

ROOT = os.path.realpath(os.path.dirname(__file__))
init = os.path.join(ROOT, 'magasin_utils', '__init__.py')
_version_re = re.compile(r'__version__\s+=\s+(.*)')
_name_re = re.compile(r'NAME\s+=\s+(.*)')

with open(init, 'rb') as f:
    content = f.read().decode('utf-8')
    VERSION = str(ast.literal_eval(_version_re.search(content).group(1)))
    NAME = str(ast.literal_eval(_name_re.search(content).group(1)))

dependency_links = set()

setup(
    name=NAME,
    version=VERSION,
    author='UNICEF',
    author_email='rapidpro@unicef.org',
    url='',
    description='Utils for databricks and magasin',
    long_description=open(os.path.join(ROOT, 'README.rst')).read(),
    zip_safe=False,
    dependency_links=list(dependency_links),
    license='BSD',
    include_package_data=True,
    classifiers=[
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
