import pymunk

from abc import ABC, abstractmethod


class PhysicObject(ABC):
    @abstractmethod
    def add(self, space: pymunk.Space) -> None:
        raise NotImplementedError


class UpdatablePhysicObject(PhysicObject, ABC):
    @abstractmethod
    def update(self, **kwargs) -> None:
        raise NotImplementedError
