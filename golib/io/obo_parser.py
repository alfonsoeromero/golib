import re
import tokenize
from ast import literal_eval
from collections import defaultdict
from io import StringIO
from typing import IO, DefaultDict, Iterator, Optional, Tuple, Union

from golib.io.parse_error import ParseError
from golib.io.stanza import Stanza
from golib.io.value import Value


class OboParser:
    """A parser for obo files."""

    def __init__(self, fp: Union[str, IO]):
        """Creates an OBO parser that reads the given file-like object.
        If you want to create a parser that reads an OBO file, do this:

          >>> import obo
          >>> parser = obo.Parser(file("gene_ontology.obo"))

        Only the headers are read when creating the parser. You can
        access these right after construction as follows:

          >>> parser.headers["format-version"]
          ['1.2']

        To read the stanzas in the file, you must iterate over the
        parser as if it were a list. The iterator yields `Stanza`
        objects.
        """
        if isinstance(fp, str):
            fp = open(fp)
        self.fp = fp
        self.line_regex = re.compile(r"\s*(?P<tag>[^:]+):\s*(?P<value>.*)")
        self.lineno: int = 0
        self._extra_line = None
        self.headers: DefaultDict = defaultdict(list)
        self._read_headers()

    def _lines(self):
        """Iterates over the lines of the file, removing
        comments and trailing newlines and merging multi-line
        tag-value pairs into a single line"""
        while True:
            self.lineno += 1
            line = self.fp.readline()
            if not line:
                break

            line = line.strip()
            if not line:
                yield line
                continue

            if line[0] == '!':
                continue
            if line[-1] == '\\':
                # This line is continued in the next line
                lines = [line[:-1]]
                finished = False
                while not finished:
                    self.lineno += 1
                    line = self.fp.readline()
                    if line[0] == '!':
                        continue
                    line = line.strip()
                    if line[-1] == '\\':
                        lines.append(line[:-1])
                    else:
                        lines.append(line)
                        finished = True
                line = " ".join(lines)
            else:
                try:
                    # Search for a trailing comment
                    comment_char = line.rindex("!")
                    if line[comment_char + 1] != '=':
                        line = line[0:comment_char].strip()
                except ValueError:
                    # No comment, fine
                    pass
            yield line

    def _parse_line(self, line: str) -> Tuple[str, Value]:
        """Parses a single line consisting of a tag-value pair
        and optional modifiers. Returns the tag name and the
        value as a `Value` object."""
        match = self.line_regex.match(line)
        if not match:
            return False
        tag, value_and_mod = match.group("tag"), match.group("value")

        # If the value starts with a quotation mark, we parse it as a
        # Python string -- luckily this is the same as an OBO string
        if value_and_mod and value_and_mod[0] == '"':
            g = tokenize.generate_tokens(StringIO(value_and_mod).readline)
            for toknum, tokval, _, (_, ecol), _ in g:
                if toknum == tokenize.STRING:
                    value = literal_eval(tokval)
                    print(value)
                    mod = (value_and_mod[ecol:].strip(), )
                    break
                raise ParseError("cannot parse string literal", self.lineno)
        else:
            value = value_and_mod
            mod = None

        value = Value(value, mod)
        return tag, value

    def _read_headers(self) -> None:
        """Reads the headers from the OBO file"""
        for line in self._lines():
            if not line or line[0] == '[':
                # We have reached the end of headers
                self._extra_line = line
                return
            key, value = self._parse_line(line)
            self.headers[key].append(value.value)

    def __iter__(self) -> Iterator[Stanza]:
        """Iterates over the stanzas in this OBO file,
        yielding a `Stanza` object for each stanza."""
        stanza: Optional[Stanza] = None
        if self._extra_line and self._extra_line[0] == '[':
            stanza = Stanza(self._extra_line[1:-1])
        for line in self._lines():
            if not line:
                continue
            if line[0] == '[':
                if stanza:
                    yield stanza
                stanza = Stanza(line[1:-1])
                continue
            tag, value = self._parse_line(line)
            stanza.add_tag_value(tag, value)
        if stanza:
            yield stanza
