import keyword
import re
from abc import ABC
from dataclasses import dataclass
from functools import wraps
from typing import *

from typing.io import *

from openapi_parser.model import Model, Filter
from openapi_parser.util.naming_conventions import field_name, const_name, class_name
from openapi_parser.util.typing_proxy import ref_name_pretty, class_name_pretty, GenericProxy

class Writer(ABC):
    JUSTIFICATION_SIZE = 80
    INDENT_SIZE = 4
    INDENT_SYMBOL = ' '
    TRIPLE_QUOT = '"""'
    TRIPLE_BACKQUOT = '```'
    NEWLINE = '\n'
    
    _indent_level: int
    def __init__(self, *args, **kwargs):
        self._indent_level = 0
        super().__init__(*args, **kwargs)
    
    @property
    def indent_level(self) -> int:
        return self._indent_level
    
    @property
    def indent_marker(self) -> str:
        return self.INDENT_SYMBOL * self.INDENT_SIZE
    
    def indent(self, increment: int = 1) -> 'Indenting':
        return Indenting(self, increment)
    
    @classmethod
    def class_name_pretty(cls, ref: Union[str, Type, GenericProxy, Model, Filter]) -> str:
        if (isinstance(ref, str)):
            return class_name(ref)
        else:
            return class_name_pretty(ref)
    @classmethod
    def field_name_pretty(cls, name: str) -> str:
        return field_name(name)
    @classmethod
    def const_name_pretty(cls, name: str) -> str:
        return const_name(name)
    @classmethod
    def ref_name_pretty(cls, ref: object, full: bool = False) -> str:
        return ref_name_pretty(ref, full=full)
    @classmethod
    def object_valid_name_filter(cls, name: str) -> str:
        if (not re.fullmatch(r'\w+', name)):
            name = re.sub(r'[\W_]+', '_', name).strip('_')
        if (not name):
            name += '_'
        if (name[0].isdigit()):
            name = 'OBJECT_' + name
        if (name in keyword.kwlist):
            name += '_'
        
        return name
    @classmethod
    def constructor(cls, constructor_name: str, **kwargs) -> str:
        return f"{constructor_name}({', '.join(f'{k}={v}' for k, v in kwargs.items())})"

# noinspection PyProtectedMember
@dataclass
class Indenting(ContextManager):
    writer: Writer
    increment: int = 1
    
    def __enter__(self):
        self.writer._indent_level += self.increment
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.writer._indent_level -= self.increment

def yielder(dumper_func: Callable[[Writer], Iterator[Optional[str]]]) -> Callable[[Writer], Iterator[Tuple[int, str]]]:
    @wraps(dumper_func)
    def wrapper(self: Writer, *args, **kwargs):
        # noinspection PyArgumentList
        yield from map(lambda line: (self.indent_level, line or ''), dumper_func(self, *args, **kwargs))
    return wrapper

def writer(yielder_func: Callable[[Writer], Iterator[Tuple[int, str]]]) -> Callable[[Writer], Optional[Iterator[str]]]:
    def writer_stream(self: Writer, *args, **kwargs) -> Iterator[str]:
        # noinspection PyArgumentList
        for level, line in yielder_func(self, *args, **kwargs):
            yield self.indent_marker * level + line
    
    @wraps(yielder_func)
    def wrapper(self: Writer, *args, file: TextIO = None, **kwargs):
        if (file is not None):
            for line in wrapper(self, *args, **kwargs, file=None):
                file.write(line)
                file.write(self.NEWLINE)
            return None
        
        else:
            return writer_stream(self, *args, **kwargs)
    
    return wrapper


__all__ = \
[
    'Indenting',
    'Writer',
    
    'writer',
    'yielder',
]
