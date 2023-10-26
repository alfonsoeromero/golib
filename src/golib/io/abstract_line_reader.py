from abc import ABC, abstractmethod
from typing import IO, Iterable, List, Union


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

    def _find(self, s: str, ch: str) -> Iterable[int]:
        """
        Find all places with `ch` in `s`
        """
        for i in range(len(s)):
            if s[i:i + len(ch)] == ch:
                yield i

    def _separator_within_quotes(self, line: str,
                                 sep: str,
                                 quote: str) -> List[bool]:
        """
        For each instance of a separator character `sep`,
        determines if a it is between two `quote` strings in `line`
        """

        quotes = list(self._find(line, quote))
        seps = list(self._find(line, sep))
        if len(quotes) <= 1:
            return [False] * len(seps)
        else:
            min_quote = min(quotes)
            max_quote = max(quotes)
            res = []
            for s in seps:
                # TODO: a smarter check
                res.append(min_quote < s < max_quote)
            return res

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
