from abc import ABC
from dataclasses import dataclass, field
from typing import *
from typing import _SpecialForm

from typing_inspect import get_origin, is_generic_type, get_args

from openapi_parser.model import Model, ModelClass, HavingPath
from .naming_conventions import *

@dataclass(repr=False, frozen=True)
class GenericProxy(ABC):
    args: Tuple[Union[Model, Type, None], ...]
    _base_class: _SpecialForm = field(init=False, repr=False, compare=False, hash=False)
    
    @property
    def base(self) -> _SpecialForm:
        return self._base_class
    @property
    def __name__(self) -> str:
        # noinspection PyProtectedMember,PyUnresolvedReferences
        return self.base._name
    
    def __repr__(self):
        return generic_repr(self.base, self.args)

@dataclass(repr=False, frozen=True)
class _UnionProxy(GenericProxy):
    args: Tuple[Union[Model, Type, None], ...]
    _base_class = Union

@dataclass(repr=False, frozen=True)
class _ListProxy(GenericProxy):
    args: Tuple[Union[ModelClass, Type]]
    _base_class = List

@dataclass(repr=False, frozen=True)
class _DictProxy(GenericProxy):
    args: Tuple[Type, Union[ModelClass, Type]]
    _base_class = Dict
    
    @property
    def key(self):
        return self.args[0]
    @property
    def value(self):
        return self.args[1]

class _UnionProxyGen:
    def __getitem__(self, items: Tuple[Union[ModelClass, Type, None], ...]) -> _UnionProxy:
        real_items = list()
        for it in items:
            is_generic, tp, args = extract_generic(it)
            if (tp == Union):
                it = UnionProxy[args]
            elif (tp == Optional):
                it = UnionProxy[args[0], None]
            else:
                list_append(real_items, it)
                continue
            
            if (isinstance(it, _UnionProxy)):
                list_extend(real_items, it.args)
        
        return _UnionProxy(tuple(real_items))

class _ListProxyGen:
    def __getitem__(self, tp: Union[ModelClass, Type]):
        return _ListProxy((tp, ))

class _DictProxyGen:
    def __getitem__(self, tp: Tuple[Type, Union[ModelClass, Type]]):
        return _DictProxy(tp)

UnionProxy = _UnionProxyGen()
ListProxy = _ListProxyGen()
DictProxy = _DictProxyGen()

T = TypeVar('T')
def list_append(lst: List[T], x: T):
    if (x not in lst):
        lst.append(x)

def list_extend(lst: List[T], it: Iterable[T]):
    for x in it:
        list_append(lst, x)

def extract_generic(tp: Type[T]) -> Tuple[bool, Type[T], Tuple[Type, ...]]:
    """
    Helper function that checks if the given type is generic,
    and if it is, expands it.
    
    Args:
        tp: `Type[T]` - potentially generic type.
    
    Returns:
        Returns a tuple of 3 values.
        
        - `bool`: **True** if the given type is `Generic`; **False** otherwise.
        - `Type[R]`: The class *T*, if *T* is not optional; and *R* if *T* is `Optional[R]`.
        - `Tuple[Type, ...]`: The tuple of class parameters used for *T*'s creation; empty tuple if it is not generic.
    
    Examples:
        ```python
        extract_generic(dict)                      # => (False, dict,    ())
        extract_generic(Dict[A, B])                # => (True,  Dict,    (A, B))
        extract_generic(Optional[int])             # => (True,  Union,   (int, None))
        extract_generic(MyClass[str])              # => (True,  MyClass, (str))
        extract_generic(Union[MyClass[str], None]) # => (True,  Union,   (MyClass[str], None))
        ```
    """
    
    if (isinstance(tp, GenericProxy)):
        # noinspection PyTypeChecker
        return True, tp.base, tp.args
    
    if (is_generic_type(tp)):
        base = get_origin(tp)
        return True, base, get_args(tp, evaluate=True)
    else:
        return False, tp, tuple()
del T

def generic_repr(cls: Union[_SpecialForm, GenericProxy], args: Tuple[Union[Type, GenericProxy, ModelClass], ...], **kwargs) -> str:
    # noinspection PyProtectedMember,PyUnresolvedReferences
    return f"{cls._name}[{', '.join(class_name_pretty(t, **kwargs) for t in args)}]"

def class_name_pretty(cls: Union[Type, GenericProxy, ModelClass], *, class_name_func: Converter = class_name, class_name_from_path_func: Converter = class_name_from_path) -> str:
    if (isinstance(cls, ModelClass)):
        if (cls.is_top_level):
            return class_name_func(cls.name)
        else:
            return class_name_from_path_func(cls.pretty_path)
    elif (isinstance(cls, HavingPath)):
        return class_name_from_path_func(cls.pretty_path)
    else:
        is_generic, base, args = extract_generic(cls)
        if (is_generic):
            return generic_repr(base, args)
        else:
            return ref_name_pretty(base)

def ref_name_pretty(obj, full: bool=False) -> str:
    if (full):
        return f'{obj.__module__}.{ref_name_pretty(obj, full=False)}'
    else:
        try:
            return f'{obj.__qualname__}'
        except AttributeError:
            return f'{obj.__name__}'


__all__ = \
[
    'GenericProxy',
    'DictProxy',
    'ListProxy',
    'UnionProxy',
    
    'class_name_pretty',
    'extract_generic',
    'generic_repr',
    'ref_name_pretty',
]
