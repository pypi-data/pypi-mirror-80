from dataclasses import Field, dataclass, field
from typing import *

from dataclasses_json import dataclass_json, LetterCase, config, DataClassJsonMixin
from functional import Option, OptionNone, Some
from typing.re import *

from openapi_parser.model import ModelSchema, ModelClass, Filter, HavingPath
from openapi_parser.util.typing_proxy import extract_generic
from openapi_parser.util.utils import SearchableEnum
from .filters import *

METADATA_KEY = 'openapi-parser'

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ModelClassImpl(ModelClass, DataClassJsonMixin):
    name: str = field(init=False)
    path: str = field(init=False)
    
    properties: Dict[str, Union[ModelSchema, Any]] = field(compare=False, hash=False)
    required_properties: List[str] = field(default_factory=list, metadata=config(field_name='required'))
    additional_properties: Union[bool, Union[ModelSchema, Any]] = True
    
    description: Optional[str] = None
    title: Optional[str] = None
    example: Optional[str] = None
    
    parents: List[ModelClass] = field(init=False, default_factory=list)
    is_top_level: bool = field(init=False, default=False)
    merged: bool = field(init=False, default=False)
    
    _pretty_path: str = field(init=False, default=None)
    @property
    def pretty_path(self) -> str:
        return self._pretty_path
    @pretty_path.setter
    def pretty_path(self, value: str):
        if (value is None):
            if (self.is_top_level):
                value = self.name
            else:
                value = self.path
        
        for f_name, f_schema in self.properties.items():
            if (isinstance(f_schema, ModelSchema)):
                for f in find_filters(f_schema.filter, HavingPath):
                    f.pretty_path = f'{value}/{f_name}/enum'
        
        self._pretty_path = value
        self.recursive_update(ModelClassImpl._update_child_pretty_path)
    
    @property
    def all_properties_iter(self) -> Iterator[Tuple[str, ModelSchema]]:
        for p in self.parents:
            yield from p.all_properties_iter
        yield from self.properties.items()
    @property
    def all_properties(self) -> Dict[str, ModelSchema]:
        return dict(self.all_properties_iter)
    
    @property
    def all_required_properties_iter(self) -> Iterator[str]:
        for p in self.parents:
            yield from p.all_required_properties_iter
        yield from self.required_properties
    @property
    def all_required_properties(self) -> List[str]:
        return list(self.all_required_properties_iter)
    
    def _update_child_pretty_path(self, child: ModelClass):
        child.pretty_path = self.pretty_path + '/' + child.name
        # if (child.path.endswith('/items')):
        #     child.pretty_path += '/item'
    
    def recursive_update(self, mapping: Callable[[ModelClass, ModelClass], Any], *, ignore_top_level: bool = True):
        for f_name, f_schema in self.properties.items():
            if (isinstance(f_schema, ModelSchema)):
                is_generic, base, args =  extract_generic(f_schema.cls)
                if (not is_generic):
                    args = [ base ]
                for cls in args:
                    if (isinstance(cls, ModelClass)):
                        if (ignore_top_level and cls.is_top_level):
                            continue
                        else:
                            mapping(self, cls)
                            cls.recursive_update(mapping, ignore_top_level=ignore_top_level)

@dataclass
class ClassRef:
    class_path: str
    class_model: ModelClass

@dataclass
class ForwardRef(ClassRef):
    @property
    def class_model(self) -> ModelClass:
        raise ValueError(f"Attempt to load forward-ref '{self.class_path}'")

class PropertyType(SearchableEnum):
    Integer = 'integer'
    Number  = 'number'
    Boolean = 'boolean'
    String  = 'string'
    Array   = 'array'
    Object  = 'object'

MISSING = object()

T = TypeVar('T')
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ModelSchemaImpl(ModelSchema, DataClassJsonMixin, Generic[T]):
    property_name: Optional[str] = field(init=False, default=None)
    property_type: Optional[PropertyType] = field(default=None, metadata=config(field_name='type'))
    property_format: Optional[str] = field(default=None, metadata=config(field_name='format'))
    description: Optional[str] = None
    title: Optional[str] = None
    example: Optional[str] = None
    
    default: Option[T] = field(default=OptionNone)
    nullable: bool = False
    read_only: bool = False
    write_only: bool = False
    
    filter: Filter[T] = field(init=False, default_factory=EmptyFilter)
    cls: Union[ModelClass, Type[T]] = field(init=False, default=Any)
    
    def __post_init__(self):
        if (not Option.is_option(self.default)):
            self.default = Some(self.default)
    
    @property
    def metadata(self) -> Dict[str, ModelSchema]:
        return { METADATA_KEY: self }
    
    @property
    def as_field(self) -> Field:
        kwargs = dict()
        if (self.default.non_empty):
            kwargs['default'] = self.default
        
        f = field(metadata=config(metadata=self.metadata, encoder=self.filter.encoder, decoder=self.filter.decoder), **kwargs)
        f.type = self.cls
        return f


def extract_metadata(f: Field) -> ModelSchema:
    return f.metadata[METADATA_KEY]


__all__ = \
[
    'ClassRef',
    'ForwardRef',
    'ModelClassImpl',
    'ModelSchemaImpl',
    'PropertyType',

    'extract_metadata',
]
