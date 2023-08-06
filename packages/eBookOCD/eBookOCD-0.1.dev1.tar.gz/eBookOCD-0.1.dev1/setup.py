"""
Copyright © 2020 Ralph Seichter

This file is part of eBookOCD.

eBookOCD is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

eBookOCD is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with eBookOCD. If not, see <https://www.gnu.org/licenses/>.
"""
from setuptools import find_packages
from setuptools import setup

from ebookocd import NAME
from ebookocd import VERSION

with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
    name=NAME,
    version=VERSION,
    install_requires=['defusedxml>=0.6.0'],
    python_requires='>=3.8',
    packages=find_packages(),
    include_package_data=True,
    entry_points={'console_scripts': ['ebookocd=ebookocd.__main__:main']},
    url='https://gitlab.com/ebookocd/ebookocd',
    license='GPLv3+',
    author='Ralph Seichter',
    author_email='ebookocd@seichter.de',
    description=(
        'Extensible utility to rewrite eBook content. Useful for fixing '
        'common mistakes made by authors and publishers alike.'
    ),
    long_description=long_description,
    long_description_content_type='text/x-rst',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
    ],
)
