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
