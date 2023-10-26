from dataclasses import dataclass
from typing import Optional


@dataclass
class Value:
    """Class representing a value and its modifiers in the OBO file

    This class has two member variables. `value` is the value itself,
    `modifiers` are the corresponding modifiers in a tuple. Currently
    the modifiers are not parsed in any way, but this might change in
    the future.
    """
    value: str
    modifiers: Optional[tuple] = ()

    def __init__(self, value: str, modifiers: Optional[tuple] = ()):
        """Creates a new value"""
        self.value = str(value)
        if modifiers:
            self.modifiers = tuple(modifiers)
        else:
            self.modifiers = None

    def __str__(self) -> str:
        """Returns the value itself (without modifiers)"""
        return str(self.value)

    def __repr__(self) -> str:
        """Returns a Python representation of this object"""
        return "%s(%r, %r)" % (self.__class__.__name__,
                               self.value, self.modifiers)
