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

from ebookocd.api import PatternReplacement
from ebookocd.transform.default import DefaultTransformer

PATTERN_REPLACEMENTS = [
    # No spam is simply spam.
    PatternReplacement(re.compile(r'\bspam\b'), 'WONDERFUL SPAM'),
]


class WonderfulSpam(DefaultTransformer):
    """ Example transformer, praising wonderful spam. """

    def setup(self) -> None:
        super().setup()
        self.pattern_replacements.extend(PATTERN_REPLACEMENTS.copy())
