from golib.config.obo_line_reader_contracts import OboLineReaderContracts
from golib.io.abstract_line_reader import AbstractLineReader


class OboLineReader(AbstractLineReader):
    """Utility for iterating through lines of an OBO file,
        doing three things:
        1.- it returns only lines with content
        2.- it removes any line that is a comment
        3.- it removes any trailing comment from a line that has
        proper content
    """

    def _line_is_useful(self, line: str) -> bool:
        return line and line.strip() and not\
            line.startswith(OboLineReaderContracts.comment_char)

    def _clean_line(self, line: str) -> str:
        if self._line_is_useful(line):
            line = line.strip()
            if OboLineReaderContracts.comment_char in line:
                return line.split(
                    OboLineReaderContracts.comment_char)[0].strip()
            else:
                return line
        return ""
