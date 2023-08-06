from typing import Callable

import stringcase

Converter = Callable[[str], str]

class_name: Converter = stringcase.pascalcase
enum_entry_name: Converter = stringcase.pascalcase
field_name: Converter = stringcase.snakecase
const_name: Converter = stringcase.constcase

def class_name_from_path(cls_path: str) -> str:
    return class_name('_'.join(cls_path.split('/')))


__all__ = \
[
    'Converter',
    
    'class_name',
    'class_name_from_path',
    'const_name',
    'enum_entry_name',
    'field_name',
]
