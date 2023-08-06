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
import sys
from zipfile import ZIP_DEFLATED
from zipfile import ZIP_STORED

NAME = 'eBookOCD'
VERSION = '0.1.dev1'


def eprint(*args, **kwargs):
    """ Print to stderr. """
    print(*args, file=sys.stderr, **kwargs)


def is_text_media_type(media_type: str) -> bool:
    """ Is a given media type considered text? """
    if not media_type:
        return False
    t = media_type.lower()
    return t.startswith('application/html') or t.startswith('application/xhtml') or t.startswith('text/')


def recursive_epub(zip_file, directory, depth, max_depth=10) -> None:
    """ Generate a compressed EPUB file containing a directory's content. """
    if depth == 0:
        # 'mimetype' must be the first file in an EPUB, and it must be uncompressed.
        zip_file.write('mimetype', compress_type=ZIP_STORED)
    elif depth >= max_depth:
        raise ValueError('Recursion crush depth reached')
    entry: os.DirEntry
    for entry in sorted(os.scandir(directory), key=lambda x: x.name):
        if entry.is_dir():
            recursive_epub(zip_file, entry.path, depth + 1, max_depth)
        elif entry.is_file() and (entry.name != 'mimetype' or depth > 0):
            zip_file.write(entry.path, compress_type=ZIP_DEFLATED)
