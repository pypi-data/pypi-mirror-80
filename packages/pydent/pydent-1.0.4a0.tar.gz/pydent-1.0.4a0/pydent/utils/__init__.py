"""Utilities

==========
utils
==========

Submodules
==========

.. autosummary::
    :toctree: _autosummary

    async_requests
    logger

"""
import pprint as pprint_module

from .loggable import condense_long_lists
from .loggable import pprint_data
from .query_builder import QueryBuilder
from pydent.utils.async_requests import make_async
from pydent.loggers import pydent_logger as logger

printer = pprint_module.PrettyPrinter(indent=1)
pprint = printer.pprint
pformat = printer.pformat


def filter_list(objlist, **kwargs):
    """Filters a list of objects based on attributes in kwargs."""
    intersection = []
    for obj in objlist:
        is_ok = True
        for k in kwargs:
            if not hasattr(obj, k):
                is_ok = False
                break
            if not getattr(obj, k) == kwargs[k]:
                is_ok = False
                break
        if is_ok:
            intersection.append(obj)
    return type(objlist)(intersection)


def url_build(*parts):
    """Join parts of a url into a string."""
    url = "/".join(p.strip("/") for p in parts)
    return url


def empty_copy(obj):
    """Return an empty copy of an object for copying purposes."""

    class Empty(obj.__class__):
        def __init__(self):
            pass

    newcopy = Empty()
    newcopy.__class__ = obj.__class__
    return newcopy
