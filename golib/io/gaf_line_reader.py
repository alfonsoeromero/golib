from typing import IO, Iterable, Union

from golib.config.gaf_line_reader_contracts import GafLineReaderContracts


class GafLineReader:
    def __init__(self, file: Union[str, IO]) -> None:
        self._file = file

    def _ensure_file(self, fp: Union[IO, str]) -> IO:
        if isinstance(fp, str):
            return open(fp)
        else:
            return fp

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

    def _line_is_useful(self, line: str) -> bool:
        return line and line.strip() and not self._line_is_comment(line)

    def _clean_line(self, line: str) -> str:
        if self._line_is_useful(line):
            line = line.strip()
            return line
        return ""

    def __iter__(self) -> Iterable[str]:
        for line in self._ensure_file(self._file):
            clean_line = self._clean_line(line)
            if clean_line:
                yield clean_line
