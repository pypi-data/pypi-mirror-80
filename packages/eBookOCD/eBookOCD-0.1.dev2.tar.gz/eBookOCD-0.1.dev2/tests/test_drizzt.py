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

from ebookocd.core import EPUBPackage
from ebookocd.transform.drizzt import Drizzt
from tests import TEST_EPUB


class DrizztTests(unittest.TestCase):
    def test_transform(self):
        package = EPUBPackage.from_zipfile(TEST_EPUB)
        # noinspection PyTypeChecker
        transformer = Drizzt()
        transformer.setup()
        package.rewrite_content(transformer)
        transformer.teardown()
        self.assertTrue(os.path.isfile(TEST_EPUB))


if __name__ == '__main__':
    unittest.main()
