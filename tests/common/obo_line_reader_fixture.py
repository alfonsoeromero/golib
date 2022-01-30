import os
from typing import List


class OboLineReaderFixture:
    @property
    def empty_file(self) -> str:
        return os.path.join(os.path.dirname(os.path.realpath(__file__)),
                            os.pardir, "data", "fake_obo_files",
                            "empty_file.obo")

    def expected_num_lines_empty_file(self) -> int:
        return 0

    def expected_lines_empty_file(self) -> List[str]:
        return []

    @property
    def comments_and_empty_lines(self) -> str:
        return os.path.join(os.path.dirname(os.path.realpath(__file__)),
                            os.pardir, "data", "fake_obo_files",
                            "comments_and_empty_lines.obo")

    def expected_num_lines_comments_and_empty_lines(self) -> int:
        return 0

    def expected_lines_comments_and_empty_lines(self) -> List[str]:
        return []

    @property
    def filled_file(self) -> str:
        return os.path.join(os.path.dirname(os.path.realpath(__file__)),
                            os.pardir, "data", "fake_obo_files",
                            "ten_lines_plus_comments_and_empty.obo")

    def expected_num_lines_filled_file(self) -> int:
        return 10

    def expected_lines_filled_file(self) -> List[str]:
        return [
            "line one",
            "line two",
            "line three",
            "line four",
            "line five",
            "line six",
            "line seven",
            "line eight",
            "line nine",
            "line ten"
        ]
