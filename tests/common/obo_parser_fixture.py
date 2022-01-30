import os
from typing import List


class OboParserFixture:
    @property
    def obo_file(self) -> str:
        return os.path.join(os.path.dirname(os.path.realpath(__file__)),
                            os.pardir, "data", "go.obo")

    @property
    def obo_file_only_header(self) -> str:
        return os.path.join(os.path.dirname(os.path.realpath(__file__)),
                            os.pardir, "data", "gene_ontology_only_headers.obo")

    def expected_headers_keys(self) -> List[str]:
        return ["format-version", "data-version", "subsetdef",
                "synonymtypedef", "default-namespace", "ontology",
                "property_value"]

    def expected_num_header_values(self) -> int:
        return 27

    def expected_num_stanzas(self) -> int:
        # total number of typedefs + terms of the included OBO file
        return 47276
