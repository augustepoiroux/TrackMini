import pymunk

from abc import ABC, abstractmethod


class PhysicObject(ABC):
    body: pymunk.Body
    shape: pymunk.Shape

    def __init_subclass__(cls, *args, **kwargs) -> None:
        """Check if all attributes are initialize correctly after init."""
        super().__init_subclass__(*args, **kwargs)

        def new_init(self, *args, init=cls.__init__, **kwargs):
            init(self, *args, **kwargs)
            for attr in PhysicObject.__annotations__:
                if attr not in self.__dict__:
                    raise AttributeError(f"{attr} is not built after init")
                elif not isinstance(self.__dict__[attr], PhysicObject.__annotations__[attr]):
                    raise TypeError(
                        f"{attr} is expected to be {PhysicObject.__annotations__[attr]} but is"
                        f" {type(self.__dict__[attr])}"
                    )

        cls.__init__ = new_init


class UpdatablePhysicObject(PhysicObject, ABC):
    @abstractmethod
    def update(self, **kwargs) -> None:
        raise NotImplementedError
