from __future__ import annotations

import inspect
from typing import Dict, Optional, Type, TypeVar

T = TypeVar('T')


class ServiceProvider(object):
    _dependencies: Dict[Type] = dict()

    def resolve(self, cls: Type[T]) -> T:
        if not self.isRegistered(cls):
            raise ValueError(f"Dependency {cls.__name__} not registered")

        if self._dependencies[cls] is not None:
            return self._dependencies[cls]
        return self.__create_instance(cls)

    def __create_instance(self, cls: type):
        constructor_signature = inspect.signature(cls.__init__)
        constructor_params = constructor_signature.parameters.values()
        dependencies = [
            self.resolve(param.annotation)
            for param in constructor_params
            if param.annotation is not inspect.Parameter.empty
        ]
        return cls(*dependencies)

    def register(self, cls: type):
        self._dependencies[cls] = None

    def register_singleton(self, cls: Type[T], implementation: T = None):
        if implementation is None:
            implementation = self.__create_instance(cls)
        self._dependencies[cls] = implementation

    def isRegistered(self, cls: Type):
        return cls in self._dependencies.keys()


class SingletonServiceProvider(ServiceProvider):
    __instance = None

    @staticmethod
    def get_instance() -> SingletonServiceProvider:
        """ Static access method. """
        if SingletonServiceProvider.__instance is None:
            SingletonServiceProvider()
        return SingletonServiceProvider.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if SingletonServiceProvider.__instance is None:
            SingletonServiceProvider.__instance = self

        else:
            raise Exception("This class is a singleton!")
