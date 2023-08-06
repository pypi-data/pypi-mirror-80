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
import tempfile
from typing import List

from ebookocd.api import PatternReplacement


def rewrite_str(line: str, pattern_replacements: List[PatternReplacement]) -> (str, int):
    s = line.strip()
    changes = 0
    for pr in pattern_replacements:
        s, n = pr.pattern.subn(pr.replacement, s)
        changes += n
    return s, changes


def rewrite_file(path: str, pattern_replacements: List[PatternReplacement]) -> int:
    """
    Rewrite a file's content. Returns n >= 0 for the number of changes
    made, and a value < 0 in case of errors.
    """
    changes = 0
    lines = 0
    dest = tempfile.NamedTemporaryFile(mode='wt', delete=False)
    with dest:
        with open(path, mode='rt') as source:
            for line in source:
                lines += 1
                s, n = rewrite_str(line, pattern_replacements)
                changes += n
                print(s, file=dest)
    shutil.copyfile(dest.name, path, follow_symlinks=False)
    os.unlink(dest.name)
    return lines
