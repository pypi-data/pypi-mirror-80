from abc import ABC
from dataclasses import Field
from typing import *

from functional import Option

class Model(ABC):
    pass

T = TypeVar('T')
Z = TypeVar('Z')
class Filter(Generic[T], ABC):
    
    def check_value(self, value: T) -> bool:
        raise NotImplementedError
    
    @property
    def decoder(self) -> Optional[Callable[[Z], T]]:
        raise NotImplementedError
    @property
    def encoder(self) -> Optional[Callable[[T], Z]]:
        raise NotImplementedError
    def decode(self, value: Z) -> T:
        raise NotImplementedError
    def encode(self, value: T) -> Z:
        raise NotImplementedError
    
    @classmethod
    def empty(cls) -> Optional['Filter[T]']:
        raise NotImplementedError
    
    @property
    def is_empty(self) -> bool:
        raise NotImplementedError
    
    def mix_with(self, f: 'Filter[T]') -> 'Filter[T]':
        raise NotImplementedError


class ModelSchema(Model, Generic[T], ABC):
    property_name: Optional[str]
    property_format: Optional[str]
    description: Optional[str]
    title: Optional[str]
    example: Optional[str]
    
    default: Option[T]
    nullable: bool
    read_only: bool
    write_only: bool
    
    filter: Optional[Filter]
    cls: Union['ModelClass', Type[T]]
    
    @property
    def metadata(self) -> Dict[str, 'ModelSchema']:
        raise NotImplementedError
    @property
    def as_field(self) -> Field:
        raise NotImplementedError


class ModelClass(Model, ABC):
    name: str
    path: str
    
    properties: Dict[str, ModelSchema]
    required_properties: List[str]
    additional_properties: Union[bool, ModelSchema]
    
    description: Optional[str]
    example: Optional[str]
    
    parents: List['ModelClass']
    is_top_level: bool
    merged: bool
    pretty_path: str
    
    @property
    def all_properties_iter(self) -> Iterator[Tuple[str, ModelSchema]]:
        raise NotImplementedError
    @property
    def all_properties(self) -> Dict[str, ModelSchema]:
        raise NotImplementedError
    
    @property
    def all_required_properties_iter(self) -> Iterator[str]:
        raise NotImplementedError
    @property
    def all_required_properties(self) -> List[str]:
        raise NotImplementedError
    
    def recursive_update(self, mapping: Callable[['ModelClass', 'ModelClass'], Any], *, ignore_top_level: bool = True):
        raise NotImplementedError


__all__ = \
[
    'Filter',
    'Model',
    'ModelClass',
    'ModelSchema',
]
