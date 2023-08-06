from .abstract_writer import *
from .class_writer import *
from .footer_writer import *
from .header_writer import *
from .model_writer import *

__all__ = [ ]

_submodules = \
[
    abstract_writer,
    class_writer,
    footer_writer,
    header_writer,
    model_writer,
]

__pdoc__ = { }
for _submodule in _submodules:
    _submodule_name = _submodule.__name__.partition(f'{__name__}.')[-1]
    __all__.extend(_submodule.__all__)
    __pdoc__[_submodule_name] = True
    _submodule.__pdoc__ = getattr(_submodule, '__pdoc__', dict())
    _extras = getattr(_submodule, '__pdoc_extras__', list())
    for _element in _submodule.__all__:
        __pdoc__[_element] = _element in _extras
