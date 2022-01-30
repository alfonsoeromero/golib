import re
import tokenize
from ast import literal_eval
from collections import defaultdict
from io import StringIO
from typing import IO, DefaultDict, Iterator, Optional, Tuple, Union
from golib.io.obo_format_error import OboFormatError

from golib.io.obo_line_reader import OboLineReader
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
        self._reader = OboLineReader(fp)
        self.line_regex = re.compile(r"\s*(?P<tag>[^:]+):\s*(?P<value>.*)")
        self.lineno: int = 0
        self.headers: DefaultDict = defaultdict(list)
        # self._read_headers()

    def _lines(self) -> str:
        """Iterates over the lines of the file"""
        for line in self._reader:
            yield line

    def _line_is_beginning_of_stanza(self, line: str) -> bool:
        if line:
            return line[0] == "["
        else:
            return False

    def _read_header_line(self, line: str) -> None:
        """Reads the headers from the OBO file"""
        if not line or self._line_is_beginning_of_stanza(line):
            # We have reached the end of headers
            return
        key, value = self._parse_line(line)
        self.headers[key].append(value.value)

    def _parse_line(self, line: str) -> Tuple[str, Value]:
        """Parses a single line consisting of a tag-value pair
        separated by ':', plus optional modifiers. Returns the
        tag name and the value as a `Value` object."""
        match = self.line_regex.match(line)
        if not match:
            raise OboFormatError(f"Cannot parse. Line '{line}' has "
                                 "unexpected format.")
        tag, value_and_mod = match.group("tag"), match.group("value")

        # If the value starts with a quotation mark, we parse it as a
        # Python string -- luckily this is the same as an OBO string
        if value_and_mod and value_and_mod[0] == '"':
            value, mod = self._extract_value_and_mod(value_and_mod)
        else:
            value = value_and_mod
            mod = None
        return tag, Value(value, mod)

    def _extract_value_and_mod(self, value_and_mod) -> Tuple[str, Value]:
        g = tokenize.generate_tokens(StringIO(value_and_mod).readline)
        for toknum, tokval, _, (_, ecol), _ in g:
            if toknum == tokenize.STRING:
                value = literal_eval(tokval)
                mod = (value_and_mod[ecol:].strip(), )
                return value, mod
            raise ParseError("Cannot parse string literal")

    def __iter__(self) -> Iterator[Stanza]:
        """Iterates over the stanzas in this OBO file,
        yielding a `Stanza` object for each stanza."""
        reading_header = True
        stanza: Optional[Stanza] = None
        for line in self._lines():
            beginning_of_stanza = self._line_is_beginning_of_stanza(line)
            if beginning_of_stanza and stanza:
                yield stanza

            reading_header = reading_header and not beginning_of_stanza

            if reading_header:
                self._read_header_line(line)
            elif beginning_of_stanza:
                stanza = Stanza(line[1:-1])
            else:
                tag, value = self._parse_line(line)
                stanza.add_tag_value(tag, value)
        if stanza:
            yield stanza
