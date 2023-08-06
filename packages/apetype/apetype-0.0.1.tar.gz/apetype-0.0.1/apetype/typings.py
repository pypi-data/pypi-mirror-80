"""Types for use in argetype configs and tasks

This module establishes ways to convert to CLI
or to do type checking for the generated calls.
"""
import abc
import typing

class Archetype(abc.ABC):
    @abc.abstractmethod
    def convert_to_CL():
        pass

    @abc.abstractmethod
    def convert_to_call():
        pass

class Cacheable(abd.ABC):
    """Abstract cache for use in function return types
    that are cacheable.
    """
    @abc.abstractmethod
    def save_to_cache():
        pass

    @abc.abstractmethod
    def load_from_cache():
        pass

    @abc.abstractmethod
    def exists():
        pass

class CACHE(Cacheable):
    def __init__(self, type, location=None, protocol=None):
        self.type = type
        self.location = location
        self.protocol = protocol

    def save_to_cache(self, key, value):
        pass

    def load_from_cache(self):
        pass

    def exists(self, key):
        # TODO Saving not yet implemented
        return False
