import dataclasses
import datetime
from typing import *

import dataclasses_json
from typing.io import *

from openapi_parser.model import ModelSchema, ModelClass
from openapi_parser.parser import OpenApiParser
from .abstract_writer import yielder, writer
from .class_writer import ClassWriter
from .footer_writer import FooterWriter
from .header_writer import HeaderWriter

class ModelWriter(ClassWriter, HeaderWriter, FooterWriter):
    
    @property
    def from_imports(self) -> Iterator[str]:
        imports = \
        [
            dataclasses.dataclass,
            dataclasses.field,
            dataclasses_json.config,
            dataclasses_json.dataclass_json,
            dataclasses_json.DataClassJsonMixin,
            dataclasses_json.LetterCase,
            datetime.datetime,
        ]
        other_imports = \
        [
            'typing.*',
        ]
        
        yield from self.objects_to_from_imports(imports)
        yield from other_imports
    
    def dump_model(self, parser: OpenApiParser) -> Iterator[str]:
        yield from self.dump_headers()
        
        exports = list()
        for path, mdl in parser.loaded_objects.items():
            if (isinstance(mdl, ModelSchema) and isinstance(mdl.cls, ModelClass) and not mdl.cls.merged):
                yield from self.dump_class(mdl.cls)
                exports.append(self.object_valid_name_filter(self.class_name_pretty(mdl.cls)))
        
        yield from self.dump_footers(exports)
    
    # region Writers
    @yielder
    def yield_model(self, parser: OpenApiParser) -> Iterator[Tuple[int, str]]:
        # noinspection PyTypeChecker
        return self.dump_model(parser)
    
    @overload
    def write_model(self, parser: OpenApiParser) -> Iterator[str]:
        pass
    # noinspection PyOverloads
    @overload
    def write_model(self, parser: OpenApiParser, *, stream: TextIO) -> None:
        pass
    @writer
    def write_model(self, parser: OpenApiParser) -> Optional[Iterator[str]]:
        # noinspection PyTypeChecker
        return self.yield_model(parser)
    # endregion


__all__ = \
[
    'ModelWriter',
]
