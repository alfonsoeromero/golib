import os
from typing import Dict


class EvalFixture:

    @property
    def gold_standard(self) -> str:
        return os.path.join(os.path.dirname(os.path.realpath(__file__)),
                            os.pardir, "data", "dog.plain_annotation")

    def expected_per_term_metrics(self) -> Dict:
        return {
            "auroc": 0.5134193310972454,
            "aupr": 0.031725892691003274,
            "f_max": 0.09305937506608873,
            "s_min": 0.20711182875508752
        }

    def expected_per_gene_metrics(self) -> Dict:
        return {
            "auroc": 0.5051466000427454,
            "aupr": 0.025326791506531908,
            "f_max": 0.0673535808896684,
            "s_min": 0.20107924420929496
        }
