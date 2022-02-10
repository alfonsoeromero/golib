import os
from typing import List


class GafParserFixture:
    @property
    def gaf_file(self) -> str:
        return os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            os.pardir,
            "data",
            "goa_dog.gaf",
        )

    @property
    def gaf_file_only_header(self) -> str:
        return os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            os.pardir,
            "data",
            "gaf_only_headers.gaf",
        )

    def expected_header_keys(self) -> List[str]:
        return ["gaf-version", "date-generated", "generated-by", "go-version"]

    def expected_num_header_values(self) -> int:
        return 4

    def expected_num_annotations(self) -> int:
        return 126142

    def expected_num_unique_go_terms(self) -> int:
        return 13343

    def expected_unique_evidence_codes(self) -> int:
        return sorted(
            [
                "IBA",
                "IC",
                "IDA",
                "IEA",
                "IEP",
                "IGI",
                "IMP",
                "IPI",
                "ISA",
                "ISS",
                "NAS",
                "ND",
                "TAS",
            ]
        )
