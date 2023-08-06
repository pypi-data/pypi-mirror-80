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
import shutil
import unittest
import uuid

from ebookocd.__main__ import bundle_epub
from ebookocd.__main__ import exit_if_exists
from ebookocd.__main__ import extract_epub
from ebookocd.__main__ import parse_args
from ebookocd.__main__ import rewrite_epub
from ebookocd.core import EPUBPackage
from tests import TEST_EPUB
from tests import TestCase


class MainTests(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.RANDOM = uuid.uuid4().hex
        self.tempdir = self.tempdir_path()
        self.tempfile = self.tempfile_path()

    def tearDown(self) -> None:
        super().tearDown()
        shutil.rmtree(self.tempdir, ignore_errors=True)
        shutil.rmtree(self.tempfile, ignore_errors=True)

    def test_exist_false(self):
        exit_if_exists(__file__ + '.BAD')
        self.assertTrue(True)

    def test_parse_invalid(self):
        with self.assertRaises(SystemExit):
            parse_args()

    def test_parse_valid(self):
        args = [self.RANDOM, '-d', 'other.epub']
        a = parse_args(args)
        self.assertEqual(self.RANDOM, a.source)
        self.assertEqual('other.epub', a.dest)

    def test_extract_exists(self):
        args = [TEST_EPUB, '-u', TEST_EPUB]
        a = parse_args(args)
        with self.assertRaises(SystemExit):
            extract_epub(a)

    def test_extract_valid(self):
        args = [TEST_EPUB, '-u', self.tempdir]
        a = parse_args(args)
        extract_epub(a)
        self.assertTrue(os.path.isdir(self.tempdir))

    def test_bundle_exists(self):
        args = [TEST_EPUB, '-z', TEST_EPUB]
        a = parse_args(args)
        with self.assertRaises(SystemExit):
            bundle_epub(a)

    def test_bundle_valid(self):
        EPUBPackage.from_zipfile(TEST_EPUB, self.tempdir)
        args = [self.tempdir, '-z', self.tempfile]
        a = parse_args(args)
        bundle_epub(a)
        self.assertTrue(os.path.isfile(self.tempfile))

    def test_transform(self):
        args = [TEST_EPUB, '-d', self.tempfile, '-t', 'ebookocd.transform.monty.WonderfulSpam']
        a = parse_args(args)
        rewrite_epub(a)
        self.assertTrue(os.path.isfile(self.tempfile))

    def test_transform_inplace(self):
        rewrite_epub(parse_args([TEST_EPUB]))
        self.assertTrue(os.path.isfile(TEST_EPUB))


if __name__ == '__main__':
    unittest.main()
