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
from argparse import ArgumentParser
from argparse import Namespace

from ebookocd import NAME
from ebookocd import VERSION
from ebookocd import eprint
from ebookocd.core import EPUBPackage
from ebookocd.transform.default import DefaultTransformer


def exit_if_exists(path: str) -> None:
    if os.path.lexists(path):
        eprint(f'{path} already exists, exiting.')
        sys.exit(1)


def extract_epub(args: Namespace) -> None:
    exit_if_exists(args.unzip)
    os.mkdir(args.unzip)
    EPUBPackage.from_zipfile(args.source, args.unzip)


def bundle_epub(args: Namespace) -> None:
    exit_if_exists(args.zip)
    EPUBPackage(args.source, []).to_zipfile(args.zip)


def rewrite_epub(args: Namespace) -> None:
    package = EPUBPackage.from_zipfile(args.source)
    if args.trans:
        transformer = _class_for_name(args.trans)()
    else:
        transformer = DefaultTransformer()
    transformer.setup()
    package.rewrite_content(transformer)
    transformer.teardown()
    if args.dest:
        destination = args.dest
    else:
        destination = args.source
    package.to_zipfile(destination)
    package.close()


def main() -> None:
    parser = ArgumentParser(prog=NAME, description=f'{NAME} {VERSION} EPUB utility')
    parser.add_argument('source', help='Source file or EPUB directory structure')
    parser.add_argument('-t', '--transform', dest='trans', metavar='CLASS',
                        help='Use specified transformer class to process content')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-d', '--dest', dest='dest', metavar='FILE', help='Destination file')
    group.add_argument('-u', '--unzip', dest='unzip', metavar='DIRECTORY',
                       help='Extract source file content into directory')
    group.add_argument('-z', '--zip', dest='zip', metavar='FILE',
                       help='Bundle source directory content as EPUB file')
    args = parser.parse_args()
    if args.unzip:
        extract_epub(args)
    elif args.zip:
        bundle_epub(args)
    else:
        rewrite_epub(args)


def _class_for_name(fully_qualified_name: str):
    """ Dynamically import a Python class. """
    segment = fully_qualified_name.split('.')
    c = __import__('.'.join(segment[:-1]))
    for segment in segment[1:]:
        c = getattr(c, segment)
    return c


if __name__ == '__main__':
    main()
