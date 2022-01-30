from dataclasses import dataclass, field
from collections import defaultdict
from typing import DefaultDict

from golib.io.value import Value


@dataclass
class Stanza:
    """Class representing an OBO stanza.

    An OBO stanza looks like this::

      [name]
      tag: value
      tag: value
      tag: value

    Values may optionally have modifiers, see the OBO specification
    for more details. This class stores the stanza name in the
    `name` member variable and the tags and values in a Python
    dict called `tags`. Given a valid stanza, you can do stuff like
    this:

      >>> stanza.name
      "Term"
      >>> print stanza.tags["id"]
      ['GO:0015036']
      >>> print stanza.tags["name"]
      ['disulfide oxidoreductase activity']

    Note that the `tags` dict contains lists associated to each
    tag name. This is because theoretically there could be more than
    a single value associated to a tag in the OBO file format.
    """
    name: str
    tags: DefaultDict = field(default_factory=lambda: defaultdict(list))

    def add_tag_value(self, tag: str, value: Value) -> None:
        """Adds a new pair (tag, value) to the contents of this stanza.

        Parameters
        ----------
        tag : str
            tag (may contain several values).
        value : Value
            one of the possibly many values corresponding to the `tag
        """
        self.tags[tag].append(value)

    def __repr__(self) -> str:
        """Returns a Python representation of this object"""
        return "%s(%r, %r)" % (self.__class__.__name__,
                               self.name, self.tags)
