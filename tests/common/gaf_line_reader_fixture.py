import os
from typing import List


class GafLineReaderFixture:
    @property
    def gaf_file(self) -> str:
        return os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            os.pardir,
            "data",
            "goa_dog.gaf",
        )

    @property
    def empty_file(self) -> str:
        return os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            os.pardir,
            "data",
            "fake_gaf_files",
            "empty_file.gaf",
        )

    def expected_useful_lines_gaf_file(self) -> int:
        return 126146

    def expected_num_lines_empty_file(self) -> int:
        return 0

    def expected_lines_empty_file(self) -> List[str]:
        return []
