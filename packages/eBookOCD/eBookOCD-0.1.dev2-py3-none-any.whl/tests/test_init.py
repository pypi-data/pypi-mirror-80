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

from ebookocd import is_text_media_type
from tests import TestCase


class InitTests(TestCase):
    def test_media_type_empty(self):
        self.assertFalse(is_text_media_type(''))

    def test_media_type_text(self):
        self.assertTrue(is_text_media_type('text/plain'))

    def test_media_type_jpeg(self):
        self.assertFalse(is_text_media_type('image/jpeg'))


if __name__ == '__main__':
    unittest.main()
