import os
from typing import Dict


class GeneOntologyFixture:

    @property
    def obo_file(self) -> str:
        return os.path.join(os.path.dirname(os.path.realpath(__file__)),
                            os.pardir, "data", "go.obo")

    @property
    def gaf_file(self) -> str:
        return os.path.join(os.path.dirname(os.path.realpath(__file__)),
                            os.pardir, "data", "goa_dog.gaf")

    def expected_num_terms_without_structure(self) -> int:
        return 0

    def expected_num_terms_with_structure(self) -> int:
        r"""
        To obtain this value independently, run this in a unix terminal:
        grep "^\[Term" go.obo | wc -l
        """
        return 47266

    def expceted_num_annotations(self) -> int:
        r"""
        To obtain this value independently, run this in a unix terminal:
        awk -F'\t' '$7 ~/EXP|IDA|IPI|IMP|IGI|IEP|TAS|IC/{print $0}' goa_dog.gaf | grep -v NOT | cut -f2,5 | sort | uniq | wc -l
        """
        return 430

    def expected_uppropagated_num_annotations(self) -> int:
        # This number was obtain with the GOTool code from S2F
        return 4226

    def expected_cache(self) -> Dict:
        return {
            "dog": {
                "global": 4226,
                "biological_process": 74,
                "cellular_component": 120,
                "molecular_function": 72,
            }
        }
