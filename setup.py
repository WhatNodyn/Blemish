# encoding: utf-8
# Blemish, an alternative client to Epitech's repository management tool
# Copyright (C) 2018 Neil Cecchini
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from blemish import __version__ as blemish_version
from setuptools import setup, find_packages
import os

blemish_readme = os.path.join(os.path.dirname(__file__), 'README.md')
with open(blemish_readme, encoding='utf-8') as fp:
    long_description = fp.read()

setup(
    name='blemish',
    version=blemish_version,

    description="An alternative client for Epitech's repository management tool",
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/WhatNodyn/Blemish',
    author='Neil Cecchini',
    author_email='stranger.neil@gmail.com',

    license='GPLv3',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 3',

        'Operating System :: OS Independent',
        'Environment :: Console',

        'Topic :: Education',
        'Topic :: Software Development :: Version Control :: Git',
        'Topic :: Software Development :: Interpreters',
        'Topic :: Utilities',
    ],

    packages=find_packages(),
)
