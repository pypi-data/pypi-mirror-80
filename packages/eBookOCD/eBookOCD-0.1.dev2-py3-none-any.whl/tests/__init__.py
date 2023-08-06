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
import unittest
from os import path
from tempfile import NamedTemporaryFile
from tempfile import TemporaryDirectory

TEST_EPUB = path.join(path.dirname(__file__), 'test.epub')


class TestCase(unittest.TestCase):
    @staticmethod
    def tempdir_path() -> str:
        p: str
        with TemporaryDirectory() as _dir:
            # Directory will be deleted when context is exited,
            # remember path beforehand.
            p = _dir
        return p

    @staticmethod
    def tempfile_path() -> str:
        p: str
        with NamedTemporaryFile(delete=True) as _file:
            # File will be deleted when context is exited,
            # remember path beforehand.
            p = _file.name
        return p
