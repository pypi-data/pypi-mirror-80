#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import ast
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open('src/xymon_client/xymon.py') as fobj:
    version = ast.literal_eval(
        re.compile(r'__version__\s*=\s*(.*)')
        .search(fobj.read()).group(1)
    )

with open('README.md') as fobj:
    README = fobj.read()





setup(
    name='xymon_client',
    version=version,
    description='a minimalist Xymon client library in Python',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Romain Dartigues',
    license='BSD 3-Clause License',
    keywords=('bb', 'BigBrother', 'xymon'),
    url='https://gitlab.com/romain-dartigues/python-xymon-client',
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Monitoring',
    ),
    package_dir={'': 'src'},
    packages=(
        'xymon_client',
    ),
    python_requires='>=2.7',
    entry_points={
        'console_scripts': [
            'xymon-client = xymon_client.__main__:main',
        ],
    },
)
