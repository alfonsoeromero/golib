from collections import defaultdict
from golib.io.gaf_line_reader import GafLineReader
from golib.io.go_annotation import GOAnnotation
from typing import IO, Optional, Union, DefaultDict, Iterator


class GafParser:
    """
    A parser of GAF files:
    http://geneontology.org/docs/go-annotation-file-gaf-format-2.2/

    It will ignore comments, but will recognize headers included
    in the comments.

    The parser should be used as an iterator that will provide
    GOAnnotation objects. The headers will be available on the
    GafParser instance after the iterarion returs the first
    GOAnnotation instance.
    """
    def __init__(self, fp: Union[str, IO]):
        self._reader = GafLineReader(fp)
        self.headers: DefaultDict = defaultdict(str)

    def _lines(self) -> str:
        for line in self._reader:
            yield line

    def _line_is_annotation(self, line: str) -> bool:
        if line:
            return line[0] != "!"
        return False

    def _read_header_line(self, line: str) -> None:
        if not line or self._line_is_annotation(line) or line == "!":
            # headers are over
            return
        key, value = line[1:].split(": ", maxsplit=1)
        self.headers[key] = value

    def __iter__(self) -> Iterator[GOAnnotation]:
        for line in self._lines():
            if not self._line_is_annotation(line):
                self._read_header_line(line)
            else:
                yield GOAnnotation.from_line(line)
