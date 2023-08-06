import json
import sys
from typing import *

import yaml

from openapi_parser.exporter import ModelWriter
from openapi_parser.parser.loader import *
from openapi_parser.parser.model import *


JUSTIFICATION_SIZE = 80
def main(args: Optional[List[str]] = None):
    if (args is None):
        args = sys.argv[1:]
    
    if (len(args) < 2):
        print(f"Not enough arguments, usage: python -m openapi_parser SCHEMA DESTINATION", file=sys.stderr)
        return 1
    
    schema_file = args[0]
    destination_file = args[1]
    
    with open(schema_file, 'rt', encoding='utf8') as f:
        if (schema_file.endswith('.json')):
            schema = json.load(f)
        elif (schema_file.endswith('.yaml') or schema_file.endswith('.yml')):
            schema = yaml.safe_load(f)
        else:
            print(f"Unsupported extension: '{''.join(schema_file.rpartition('.')[1:])}'", file=sys.stderr)
            return 1
    
    parser = OpenApiParser(schema)
    parser.load_all()
    writer = ModelWriter()
    
    for path, mdl in parser.loaded_objects.items():
        print(('# ' + type(mdl).__name__ + (f" '{mdl.property_name}'" if isinstance(mdl, ModelSchemaImpl) else '')).ljust(JUSTIFICATION_SIZE, ' ') + f" -- '{path}'")
    print('# ' + '=' * JUSTIFICATION_SIZE)
    print('')
    
    with open(destination_file, 'wt', encoding='utf8') as output:
        writer.write_model(parser, file=output)
    
    return 0

if (__name__ == '__main__'):
    exit_code = main()
    exit(exit_code)
