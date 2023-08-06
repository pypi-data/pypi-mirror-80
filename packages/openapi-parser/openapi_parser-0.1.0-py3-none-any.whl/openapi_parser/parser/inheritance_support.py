import warnings
from dataclasses import dataclass, Field, field
from functools import partial, reduce
from itertools import chain
from typing import *
from typing import Optional, Dict, List

from dataclasses_json import dataclass_json, LetterCase, DataClassJsonMixin, config
from functional import Option, OptionNone, Some

from openapi_parser.model import Filter
from openapi_parser.util.utils import mix_options, dict_safe_merge
from .errors import OpenApiLoaderError
from .filters import FilterImpl
from .model import ModelClassImpl


@dataclass(frozen=True)
class UnableToBuildDiscriminator(OpenApiLoaderError):
    filter: 'InheritanceFilter'
    
    @property
    def message(self) -> str:
        return f"Unable to build a discriminator decoder for filter '{self.filter}'"
    
    def __post_init__(self):
        super().__init__(self.message)

@dataclass(frozen=True)
class InvalidAlternativeTypes(UnableToBuildDiscriminator, TypeError):
    filter: 'InheritanceFilter'
    invalid_type: Union[ModelClassImpl, Type]
    
    @property
    def message(self) -> str:
        return f"{super().message}: Only Dict[str, Any] and ModelClass are supported, got: {self.invalid_type}"
    
    def __post_init__(self):
        super().__init__(self.message)


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class DiscriminatorObject(DataClassJsonMixin):
    property_name: str
    mapping: Optional[Dict[str, str]] = None
    
    def mix_with(self, other: 'DiscriminatorObject') -> 'DiscriminatorObject':
        if (self.property_name != other.property_name):
            # ToDo: Different discriminator data
            raise ValueError
        
        return DiscriminatorObject \
        (
            property_name = self.property_name,
            mapping = mix_options(self.mapping, other.mapping).map(dict_safe_merge).as_optional,
        )

T = TypeVar('T')
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class InheritanceFilter(FilterImpl[T], Generic[T]):
    discriminator: Optional[DiscriminatorObject] = None
    all_of: Optional[List[Field]] = None
    any_of: Optional[List[Field]] = None
    one_of: Optional[List[Field]] = None
    filter_not: Optional[Field] = field(default=None, metadata=config(field_name='not'))
    
    def check_value(self, value: T):
        warnings.warn(RuntimeWarning("InheritanceFilter is not implemented"))
        return True
    
    def decoder(self):
        if (self.discriminator is None):
            return None
        
        # ToDo: Discriminator support
        raise NotImplementedError("Discriminator support is not yet implemented")
    
    def mix_with(self, f: Filter[T]) -> Filter[T]:
        if (isinstance(f, InheritanceFilter)):
            filter_not = mix_options(self.filter_not, f.filter_not)
            filter_all_mixin = OptionNone
            if (filter_not.non_empty):
                if (len(filter_not.get) > 1):
                    filter_not = OptionNone
                    filter_all_mixin = Some([])
                    # ToDo: Mix
                    raise NotImplementedError("Mixing of multiple NOT is not currently supported")
            
            return InheritanceFilter \
            (
                discriminator = mix_options(self.discriminator, f.discriminator).map(lambda lst: reduce(InheritanceFilter.mix_with, lst)).as_optional,
                all_of        = mix_options(self.all_of, f.all_of, filter_all_mixin).map(chain.from_iterable).map(list).as_optional,
                any_of        = mix_options(self.any_of, f.any_of).map(chain.from_iterable).map(list).as_optional,
                one_of        = mix_options(self.one_of, f.one_of).map(chain.from_iterable).map(list).as_optional,
                filter_not    = filter_not.as_optional,
            )

def get_class_name(t: Union[Type, ModelClassImpl]) -> str:
    if (isinstance(t, ModelClassImpl)):
        return t.name
    else:
        return t.__name__

def discriminator_decoder(filter: InheritanceFilter[T]) -> Callable[[Dict[str, Any]], T]:
    items = Option(filter.any_of).get_or_else(list()) + Option(filter.one_of).get_or_else(list()) + Option(filter.all_of).get_or_else(list())
    for it in items:
        if (it.type != dict and not isinstance(it.type, ModelClassImpl)):
            raise InvalidAlternativeTypes(filter, it.type)
    
    mapping = Option(filter.discriminator.mapping).get_or_else({ get_class_name(it.type): it.type for it in items })
    # noinspection PyTypeChecker
    return partial(discriminator_decode, discriminator_field=filter.discriminator.property_name, discriminator_mappings=mapping)

T = TypeVar('T')
def discriminator_decode(data: Dict[str, Any], *, discriminator_field: str, discriminator_mappings: Dict[str, Union[ModelClassImpl, Type[T]]]) -> T:
    pass


__all__ = \
[
    'DiscriminatorObject',
    'InheritanceFilter',
    'InvalidAlternativeTypes',
    'UnableToBuildDiscriminator',

    'discriminator_decode',
    'discriminator_decoder',
]
