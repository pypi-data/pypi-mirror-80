from abc import ABC
from typing import *

from typing.io import *

from .abstract_writer import Writer, yielder, writer

class FooterWriter(Writer, ABC):
    @property
    def exports(self) -> Iterator[str]:
        return ()
    
    def dump_footers(self, items: Iterable[str] = None, *, ordered: bool = None) -> Iterator[str]:
        if (items is None):
            items = self.exports
        if (ordered is None):
            ordered = True
        if (ordered):
            items = sorted(items)
        
        yield
        yield '__all__ = \\'
        yield '['
        with self.indent():
            yield from map("'{}',".format, items)
        yield ']'
    
    # region Writers
    @yielder
    def yield_footers(self, items: Iterable[str] = None, *, ordered: bool = None) -> Iterator[Tuple[int, str]]:
        # noinspection PyTypeChecker
        return self.dump_footers(items, ordered=ordered)
    
    @overload
    def write_footers(self, items: Iterable[str] = None, *, ordered: bool = None) -> Iterator[str]:
        pass
    # noinspection PyOverloads
    @overload
    def write_footers(self, items: Iterable[str] = None, *, ordered: bool = None, stream: TextIO) -> None:
        pass
    @writer
    def write_footers(self, items: Iterable[str] = None, *, ordered: bool = None) -> Optional[Iterator[str]]:
        # noinspection PyTypeChecker
        return self.yield_footers(items, ordered=ordered)
    # endregion


__all__ = \
[
    'FooterWriter',
]
