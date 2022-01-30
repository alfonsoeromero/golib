from typing import IO, Iterable, Union

from golib.config.obo_line_reader_contracts import OboLineReaderContracts


class OboLineReader:
    """Utility for iterating through lines of an OBO file,
        doing three things:
        1.- it returns only lines with content
        2.- it removes any line that is a comment
        3.- it removes any trailing comment from a line that has
        proper content
    """

    def __init__(self, file: Union[IO, str]) -> None:
        """Constructor

        Parameters
        ----------
        file : Union[IO, str]
            file name or file object that we want to read.
        """
        self._file = file

    def _ensure_file(self, fp: Union[IO, str]) -> IO:
        if isinstance(fp, str):
            return open(fp)
        else:
            return fp

    def _line_is_useful(self, line: str) -> bool:
        return line and line.strip() and not\
            line.startswith(OboLineReaderContracts.comment_char)

    def _clean_line(self, line: str) -> str:
        line = line.strip()
        if OboLineReaderContracts.comment_char in line:
            return line.split(OboLineReaderContracts.comment_char)[0].strip()
        else:
            return line

    def __iter__(self) -> Iterable[str]:
        """Main iterable's method, yields clean and non-empty lines

        Returns
        -------
        Iterable[str]
            different lines present in the file

        Yields
        -------
        Iterator[Iterable[str]]
            string objects
        """
        for line in self._ensure_file(self._file):
            if self._line_is_useful(line):
                clean_line = self._clean_line(line)
                if clean_line:
                    yield clean_line
