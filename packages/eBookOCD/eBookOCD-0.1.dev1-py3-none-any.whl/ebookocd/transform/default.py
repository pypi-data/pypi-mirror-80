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
import re
from typing import List

from ebookocd.api import PatternReplacement
from ebookocd.api import TransformerMixin
from ebookocd.transform import rewrite_file as _rewrite_file
from ebookocd.transform import rewrite_str as _rewrite_str

""" Patterns found in many ebooks. """
PATTERN_REPLACEMENTS = [
    # Consecutive spaces, not including &nbsp;
    PatternReplacement(re.compile(r'[ \t\r\n]+'), ' '),
    # Horizontal ellipsis
    PatternReplacement(re.compile(r' ?(\. ){3,}'), '\u2026'),
]


class DefaultTransformer(TransformerMixin):
    def __init__(self) -> None:
        self.pattern_replacements: List[PatternReplacement] = []

    def setup(self) -> None:
        self.pattern_replacements.extend(PATTERN_REPLACEMENTS.copy())

    def teardown(self) -> None:
        pass

    def rewrite_file(self, filename: str) -> None:
        _rewrite_file(filename, self.pattern_replacements)

    def rewrite_str(self, string: str) -> None:
        _rewrite_str(string, self.pattern_replacements)
