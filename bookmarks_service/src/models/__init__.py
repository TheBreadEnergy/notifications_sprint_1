import sys
from typing import Sequence, Type, TypeVar

from beanie import Document

from .bookmark import Bookmark  # noqa: F401
from .film_like import FilmLike  # noqa: F401
from .review import Review  # noqa: F401

DocType = TypeVar("DocType", bound=Document)


def gather_documents() -> Sequence[Type[DocType]]:
    from inspect import getmembers, isclass

    return [
        doc
        for _, doc in getmembers(sys.modules[__name__], isclass)
        if issubclass(doc, Document) and doc.__name__ != "Document"
    ]
