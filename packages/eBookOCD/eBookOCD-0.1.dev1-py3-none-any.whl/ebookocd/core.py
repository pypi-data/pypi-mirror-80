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
import tempfile
from typing import List
from typing import Optional
from xml.etree.ElementTree import ElementTree
from zipfile import ZipFile
from zipfile import ZipInfo

from defusedxml.ElementTree import parse

from ebookocd import is_text_media_type
from ebookocd import recursive_epub
from ebookocd.api import TransformerMixin


class EPUBPackage:
    def __init__(self, directory: str, zip_info_list: List[ZipInfo]) -> None:
        self.directory = directory
        self.zip_info_list = zip_info_list

    @classmethod
    def from_zipfile(cls, zip_path: str, directory: str = '') -> 'EPUBPackage':
        """ Fabricate object from an existing EPUB file. """
        with ZipFile(zip_path) as zf:
            if not directory:
                directory = tempfile.TemporaryDirectory(prefix='epubutil').name
            zf.extractall(path=directory)
            return EPUBPackage(directory, zf.infolist())

    def to_zipfile(self, zip_path: str) -> None:
        """ Create ZIP based on an existing ZipInfo list. """
        with ZipFile(zip_path, 'w', allowZip64=False) as zip_file:
            cwd = os.getcwd()
            os.chdir(self.directory)
            if self.zip_info_list:
                # Content is based on existing ZipInfo list
                for zip_info in self.zip_info_list:
                    zip_file.write(zip_info.filename, compress_type=zip_info.compress_type)
            else:
                # Scan directory for content
                recursive_epub(zip_file, directory='.', depth=0)
            zip_file.close()
            os.chdir(cwd)

    def rewrite_content(self, transformer: TransformerMixin) -> None:
        cd = Container(parent=self)
        cd.from_xml()
        element = cd.element_tree.findall('.//{*}rootfiles/{*}rootfile')[0]
        package = Package(parent=self, relative_path=element.attrib['full-path'])
        package.from_xml()
        package.process_text_files(transformer)

    def close(self):
        del self.directory


class XmlBase:
    def __init__(self, parent: EPUBPackage, relative_path: str) -> None:
        self.element_tree: Optional[ElementTree] = None
        self.parent = parent
        self.relative_path = relative_path

    def from_xml(self):
        self.element_tree = parse(os.path.join(self.parent.directory, self.relative_path))


class Container(XmlBase):
    def __init__(self, parent: EPUBPackage) -> None:
        super().__init__(parent, os.path.join('META-INF', 'container.xml'))


class Package(XmlBase):
    def _text_file_paths(self) -> List[str]:
        paths: List[str] = []
        for item in self.element_tree.findall('.//{*}manifest/{*}item'):
            if is_text_media_type(item.attrib['media-type']):
                paths.append(os.path.join(self.parent.directory, item.attrib['href']))
        return paths

    def process_text_files(self, transformer: TransformerMixin):
        assert transformer is not None, 'no transformer specified'
        for path in self._text_file_paths():
            transformer.rewrite_file(path)
