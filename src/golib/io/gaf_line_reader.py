from golib.config.gaf_line_reader_contracts import GafLineReaderContracts
from golib.io.abstract_line_reader import AbstractLineReader


class GafLineReader(AbstractLineReader):
    """
    A parser of lines belonging to a GAF file:
    http://geneontology.org/docs/go-annotation-file-gaf-format-2.2/

    It will ignore comments, but will recognize headers included
    in the comments.
    """

    def _line_is_header(self, line: str) -> bool:
        if GafLineReaderContracts.header_separation_str in line:
            sep_location = line.index(GafLineReaderContracts.comment_char)
            return (
                line[0] == GafLineReaderContracts.comment_char
                and len(line.strip()) > sep_location + 2
            )
        return False

    def _line_is_comment(self, line: str) -> bool:
        if line[0] == GafLineReaderContracts.comment_char:
            return not self._line_is_header(line)
        return False

    def _line_is_useful(self, line: str) -> bool:
        return line and line.strip() and not self._line_is_comment(line)

    def _clean_line(self, line: str) -> str:
        if self._line_is_useful(line):
            return line.strip()
        return ""
