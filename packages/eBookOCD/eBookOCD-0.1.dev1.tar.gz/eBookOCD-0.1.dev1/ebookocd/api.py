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
from abc import ABC
from abc import abstractmethod
from re import Pattern


class PatternReplacement:
    def __init__(self, pattern: Pattern, replacement: str) -> None:
        super().__init__()
        self.pattern = pattern
        self.replacement = replacement


class TransformerMixin(ABC):
    @abstractmethod
    def setup(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def teardown(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def rewrite_file(self, filename: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def rewrite_str(self, string: str) -> None:
        raise NotImplementedError
