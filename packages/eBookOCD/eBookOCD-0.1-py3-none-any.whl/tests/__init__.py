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
import os
import unittest
from filecmp import dircmp
from tempfile import NamedTemporaryFile
from tempfile import TemporaryDirectory

from ebookocd import eprint

TEST_EPUB = os.path.join(os.path.dirname(__file__), 'test.epub')


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


class DirectoryComparison:
    def __init__(self, dc: dircmp) -> None:
        self._dircmp = dc

    def contents_match(self) -> bool:
        for name in self._dircmp.diff_files:
            left = os.path.join(self._dircmp.left, name)
            right = os.path.join(self._dircmp.right, name)
            eprint(f'File content mismatch:\n  {left}\n  {right}')
        if self._dircmp.diff_files:
            return False
        for dc in self._dircmp.subdirs.values():
            if not DirectoryComparison(dc).contents_match():
                return False
        # All tests passed
        return True
