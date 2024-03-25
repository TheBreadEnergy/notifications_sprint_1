from typing import Callable, Type

dependencies: dict[Type | Callable, Callable] = {}


def add_factory_to_mapper(class_: Type | Callable):
    def _add_factory_to_mapper(func: Callable):
        dependencies[class_] = func
        return func

    return _add_factory_to_mapper
