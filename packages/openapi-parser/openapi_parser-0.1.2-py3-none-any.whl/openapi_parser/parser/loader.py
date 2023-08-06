from datetime import datetime
from typing import *

from functional import Option

from openapi_parser.model import Model, ModelClass, Filter, ModelSchema
from openapi_parser.util._backports import singledispatchmethod
from openapi_parser.util.typing_proxy import *
from .date_formats import DateFormatName
from .errors import *
from .filters import *
from .inheritance_support import InheritanceFilter
from .model import *

class OpenApiParser:
    name: Optional[str]
    data: Dict[str, Any]
    
    loaded_objects: Dict[str, Model]
    unresolved_forward_refs: Dict[str, List[ModelClass]]
    
    def __init__(self, data: Dict[str, Any], name: str = None):
        self.data = data
        self.name = name
        
        self.loaded_objects = dict()
        self.unresolved_forward_refs = dict()
    
    def load_all(self):
        self.load_schemas()
    
    def load_schemas(self):
        try:
            schemas = self.load_object('#/components/schemas')
        except UnresolvedReference:
            pass
        else:
            for s in schemas:
                self.load_schema(f'#/components/schemas/{s}')
    
    def load_data(self, path: str, source: Dict[str, Any] = None, *, base_path: str = None, **kwargs) -> Any:
        if (base_path is None):
            base_path = path
        
        left, sep, right = path.partition('/')
        if (left == '#'):
            if (not sep):
                return self.data
            else:
                return self.load_data(right, self.data, base_path=base_path, **kwargs)
        
        elif (source is None):
            raise InvalidReferenceFormat(base_path)
        elif (not sep):
            return source[left]
        elif (not isinstance(source, dict)):
            raise InvalidReference(base_path)
        elif (left not in source):
            raise UnresolvedReference(base_path)
        else:
            return self.load_data(right, source[left], base_path=base_path, **kwargs)
    
    def load_object(self, path: str, source: Dict[str, Any] = None, **kwargs) -> Dict[str, Any]:
        result = self.load_data(path, source, **kwargs)
        if (not isinstance(result, dict)):
            raise InvalidReference(path)
        return result
    
        pass
    
    @singledispatchmethod
    def load_class(self, class_data: Dict[str, Any], path: str, *, is_top_level: bool = False, **kwargs) -> ModelClass:
        return self._load_class(class_data, path, is_top_level=is_top_level, **kwargs)
    
    @load_class.register
    def _(self, path: str, *, is_top_level: bool = True, **kwargs) -> ModelClass:
        return self.load_class(self.load_object(path), path, is_top_level=is_top_level, **kwargs)
    
    def _load_class(self, class_data: Dict[str, Any], path: str, *, is_top_level: bool, force_name: Optional[str] = None, **kwargs) -> ModelClass:
        if (force_name is not None):
            name = force_name
        else:
            _, _, name = path.rpartition('/')
        
        loaded_class = ModelClassImpl.from_dict(class_data)
        loaded_class.name = name
        loaded_class.path = path
        for p, d in loaded_class.properties.items(): # type: str, Dict[str, Any]
            loaded_class.properties[p] = self.load_schema(d, f'{path}/properties/{p}')
        if (isinstance(loaded_class.additional_properties, dict)):
            loaded_class.additional_properties = self.load_schema(loaded_class.additional_properties, f'{path}/additionalProperties')
        
        loaded_class.is_top_level = is_top_level
        loaded_class.pretty_path = name if force_name else None
        return loaded_class
    
    def load_ref(self, path: str, **kwargs) -> ModelSchema:
        if (path in self.loaded_objects):
            return self.loaded_objects[path]
        else:
            return self.load_schema(self.load_object(path), path, is_top_level=True, **kwargs)
    
    @singledispatchmethod
    def load_schema(self, schema_data: Dict[str, Any], path: str, *, is_top_level: bool = False, **kwargs) -> ModelSchema:
        if ('$ref' in schema_data):
            return self.load_ref(schema_data['$ref'], **kwargs)
        else:
            obj = self.load_schema_object(schema_data, path, is_top_level=is_top_level, **kwargs)
            self._resolve_ref(obj, path, **kwargs)
            return obj
    
    @load_schema.register
    def _(self, path: str, **kwargs) -> ModelSchema:
        return self.load_ref(path, **kwargs)
    
    def _load_fields(self, f: Optional[List[Dict[str, Any]]], path: str, **kwargs) -> Optional[List[ModelSchema]]:
        if (f is not None):
            return list(self._load_fields_iter(f, path, **kwargs))
        else:
            return None
    
    def _load_fields_iter(self, f: List[Dict[str, Any]], path: str, **kwargs) -> Iterator[ModelSchema]:
        for i, d in enumerate(f):
            yield self.load_schema(d, f'{path}/.{i}', **kwargs)
    
    def _merge_classes(self, classes: List[ModelSchema], path: str, *, is_top_level: bool, force_name: Optional[str] = None, **kwargs) -> Tuple[ModelClass, Filter]:
        if (force_name is not None):
            name = force_name
        else:
            _, _, name = path.rpartition('/')
        
        m = ModelClassImpl(properties={ })
        m.name = name
        m.path = path
        m.is_top_level = is_top_level
        filter = EmptyFilter()
        
        for c in classes:
            filter = filter.mix_with(c.filter)
            
            if (isinstance(c.cls, ModelClass)):
                if (m.additional_properties == True):
                    m.additional_properties = c.cls.additional_properties
                elif (m.type.additional_properties != c.cls.additional_properties):
                    # ToDo: Additional properties conflict error
                    raise ValueError
                
                if (c.cls.is_top_level):
                    m.parents.append(c.cls)
                else:
                    for prop_name, prop_field in c.cls.properties.items():
                        if (prop_name in m.properties and prop_field != m.properties[prop_name]):
                            # ToDo: Field conflict error
                            raise ValueError
                        m.properties[prop_name] = prop_field
                    
                    m.required_properties += c.cls.required_properties
                    if (c.cls.example is not None):
                        m.example = c.cls.example
                    if (c.cls.description is not None):
                        m.example = c.cls.example
                    c.cls.merged = True
            
            else:
                is_generic, tp, args = extract_generic(c.cls)
                if (tp == dict):
                    if (m.additional_properties == False):
                        # ToDo: Additional properties conflict error
                        raise ValueError
                
                elif (tp == Dict):
                    K, V = args
                    if (K == str and isinstance(V, ModelSchema)):
                        if (m.additional_properties == True):
                            m.additional_properties = V
                        elif (m.additional_properties != V):
                            # ToDo: Additional properties conflict error
                            raise ValueError
                
                else:
                    # ToDo: Type error
                    raise ValueError
        
        m.pretty_path = None
        return m, filter
    
    def load_schema_object(self, schema_data: Dict[str, Any], path: str, *, is_top_level: bool, force_name: Optional[str] = None, **kwargs) -> ModelSchema:
        if (force_name is not None):
            name = force_name
        else:
            _, _, name = path.rpartition('/')
        
        field_data = ModelSchemaImpl.from_dict(schema_data)
        field_data.property_name = name
        inheritance_data = InheritanceFilter.from_dict(schema_data)
        if (not inheritance_data.is_empty):
            inheritance_data.all_of = self._load_fields(inheritance_data.all_of, path + '/allOf')
            inheritance_data.any_of = self._load_fields(inheritance_data.any_of, path + '/anyOf')
            inheritance_data.one_of = self._load_fields(inheritance_data.one_of, path + '/oneOf')
            if (inheritance_data.filter_not is not None):
                inheritance_data.filter_not: Dict[str, Any]
                inheritance_data.filter_not = self.load_schema(inheritance_data.filter_not, path + '/not')
        
        if (field_data.property_type is None):
            field_data.cls = Any
        
        elif (field_data.property_type == PropertyType.Integer):
            field_data.cls = int
            field_data.filter = NumericFilter.from_dict(schema_data)
        
        elif (field_data.property_type == PropertyType.Number):
            field_data.cls = float
            field_data.filter = NumericFilter.from_dict(schema_data)
        
        elif (field_data.property_type == PropertyType.String):
            if (DateFormatName.contains_value(field_data.property_format)):
                field_data.cls = datetime
                field_data.filter = DateFilter.from_dict(schema_data)
            else:
                if (field_data.property_format in ('byte', 'binary')):
                    field_data.cls = bytes
                else:
                    field_data.cls = str
                field_data.filter = StringFilter.from_dict(schema_data)
        
        elif (field_data.property_type == PropertyType.Boolean):
            field_data.cls = bool
        
        elif (field_data.property_type == PropertyType.Array):
            if ('items' in schema_data):
                items = self.load_schema(schema_data['items'], path + '/items', force_name=field_data.property_name + 'Item')
                field_data.cls = ListProxy[items.cls]
            else:
                field_data.cls = list
            field_data.filter = ArrayFilter.from_dict(schema_data)
        
        elif (field_data.property_type == PropertyType.Object):
            additional_properties: Union[bool, Dict[str, Any]] = schema_data.get('additionalProperties', True)
            if ('properties' in schema_data):
                field_data.cls = self.load_class(schema_data, path, is_top_level=is_top_level, force_name=field_data.property_name)
            elif (additional_properties == False):
                raise InvalidSchemaFields(path, "'additionalProperties=False' is not allowed in combination with missing 'properties' for 'object' invalid_type")
            elif (isinstance(additional_properties, dict)):
                cls = self.load_schema(additional_properties, path + '/additionalProperties', force_name=field_data.property_name + 'Item')
                field_data.cls = DictProxy[str, cls]
                field_data.filter = DictFilter.from_dict(schema_data)
            else:
                field_data.cls = dict
                field_data.filter = DictFilter.from_dict(schema_data)
        
        field_data.filter = EmptyFilter().mix_with(field_data.filter).mix_with(inheritance_data)
        
        if (inheritance_data.any_of is not None or inheritance_data.one_of is not None):
            if (inheritance_data.all_of is not None):
                raise InvalidSchemaFields(path, f"allOf is not allowed in combination with oneOf/anyOf")
            
            items = Option(inheritance_data.any_of).get_or_else(list()) + Option(inheritance_data.one_of).get_or_else(list())
            field_data.cls = UnionProxy[tuple(items)]
        
        elif (inheritance_data.all_of is not None and field_data.cls == Any):
            field_data.cls, inh_filter = self._merge_classes(inheritance_data.all_of, path, is_top_level=is_top_level, force_name=field_data.property_name)
            inheritance_data = inheritance_data.mix_with(inh_filter)
        
        field_data.filter = field_data.filter.mix_with(inheritance_data)
        if ('enum' in schema_data):
            enum_filter = EnumFilter.from_dict(schema_data)
            enum_filter.path = path + '/enum'
            enum_filter.pretty_path = path + '/enum'
            field_data.filter = field_data.filter.mix_with(enum_filter)
        
        return field_data
    
    def _resolve_ref(self, loaded_class: Model, path: str, **kwargs):
        if (path in self.unresolved_forward_refs):
            for cls in self.unresolved_forward_refs[path]:
                for f in cls.properties:
                    f.type = loaded_class
            del self.unresolved_forward_refs[path]
        
        self.loaded_objects[path] = loaded_class


__all__ = \
[
    'OpenApiParser',
]
