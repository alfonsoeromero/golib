from unittest import TestCase
from goapfp.core.gene_ontology import GeneOntology
from goapfp.eval.classification import per_gene, per_term
from tests.common.eval_fixture import EvalFixture
from tests.common.gene_ontology_fixture import GeneOntologyFixture
import numpy as np


class TestClassification(TestCase):

    def setUp(self) -> None:
        self._fixture = EvalFixture()
        self._go_fixture = GeneOntologyFixture()

    def test_per_gene_metrics(self):
        labels = self._fixture.gold_standard
        obo = self._go_fixture.obo_file
        rng = np.random.default_rng(seed=0)

        go = GeneOntology(obo)
        go.build_ontology()
        go.load_annotation_file(labels, "dog_binary")
        go.up_propagate_annotations("dog_binary")
        annotations = go.annotations("dog_binary")

        y_table = annotations.pivot_table(index="Protein",
                                          columns="GO ID",
                                          values="Score").fillna(0.0)
        ic = []
        for go_term in y_table.columns:
            ic.append(go.find_term(go_term).information_content("dog_binary"))
        ic = np.array(ic)
        y_test = y_table.values
        y_pred = rng.random(size=y_test.shape)
        res = per_gene(y_pred, y_test, information_content=ic)

        sut = {}
        for m in res.keys():
            sut[m] = np.mean(res[m])

        expected_metrics = self._fixture.expected_per_gene_metrics()

        self.assertEqual(sut, expected_metrics)

    def test_per_term_metrics(self):
        labels = self._fixture.gold_standard
        obo = self._go_fixture.obo_file
        rng = np.random.default_rng(seed=0)

        go = GeneOntology(obo)
        go.build_ontology()
        go.load_annotation_file(labels, "dog_binary")
        go.up_propagate_annotations("dog_binary")
        annotations = go.annotations("dog_binary")

        y_table = annotations.pivot_table(index="Protein",
                                          columns="GO ID",
                                          values="Score").fillna(0.0)
        ic = []
        for go_term in y_table.columns:
            ic.append(go.find_term(go_term).information_content("dog_binary"))
        ic = np.array(ic)
        y_test = y_table.values
        y_pred = rng.random(size=y_test.shape)
        res = per_term(y_pred, y_test, information_content=ic)

        sut = {}
        for m in res.keys():
            sut[m] = np.mean(res[m])

        expected_metrics = self._fixture.expected_per_term_metrics()

        self.assertEqual(sut, expected_metrics)
