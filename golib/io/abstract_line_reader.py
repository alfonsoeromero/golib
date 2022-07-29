from abc import ABC, abstractmethod
from typing import IO, Iterable, Union


class AbstractLineReader(ABC):
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

    @abstractmethod
    def _clean_line(self, line: str) -> str:
        """To be implemented in subclasses"""

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
        with self._ensure_file(self._file) as f:
            for line in f:
                clean_line = self._clean_line(line)
                if clean_line:
                    yield clean_line
