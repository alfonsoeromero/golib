from unittest import TestCase

from golib.core.gene_ontology import GeneOntology

from tests.common.gene_ontology_fixture import GeneOntologyFixture

class TestGeneOntology(TestCase):

    def setUp(self) -> None:
        self._fixture = GeneOntologyFixture()

    def test_initialization_state(self):
        obo_file = self._fixture.obo_file
        sut = GeneOntology(obo_file)

        expected_num_terms_without_structure = self._fixture.expected_num_terms_without_structure()

        actual_num_terms = len(sut._terms)

        self.assertEqual(actual_num_terms, expected_num_terms_without_structure)

    def test_structure_state(self):
        obo_file = self._fixture.obo_file
        sut = GeneOntology(obo_file)
        sut.build_ontology()

        expected_num_terms_with_structure = self._fixture.expected_num_terms_with_structure()

        actual_num_terms = len(sut._terms)

        self.assertEqual(actual_num_terms, expected_num_terms_with_structure)

    def test_num_annotations(self):
        obo_file = self._fixture.obo_file
        gaf_file = self._fixture.gaf_file

        sut = GeneOntology(obo_file)
        sut.build_ontology()
        sut.load_gaf_file(gaf_file, "dog")

        expected_num_annotations = self._fixture.expceted_num_annotations()
        actual_num_annotations = sut.annotations("dog").shape[0]

        self.assertEqual(actual_num_annotations, expected_num_annotations)

    def test_uppropagated_num_annotations(self):
        obo_file = self._fixture.obo_file
        gaf_file = self._fixture.gaf_file

        sut = GeneOntology(obo_file)
        sut.build_ontology()
        sut.load_gaf_file(gaf_file, "dog")
        sut.up_propagate_annotations("dog")

        excpected_uppropagated_num_annotations = self._fixture.expected_uppropagated_num_annotations()
        actual_num_annotations = sut.annotations("dog").shape[0]

        self.assertEqual(actual_num_annotations, excpected_uppropagated_num_annotations)

    def test_annotation_cache(self):
        obo_file = self._fixture.obo_file
        gaf_file = self._fixture.gaf_file

        sut = GeneOntology(obo_file)
        sut.build_ontology()
        sut.load_gaf_file(gaf_file, "dog")
        sut.up_propagate_annotations("dog")

        expected_cache = self._fixture.expected_cache()
        self.assertEqual(sut._annotation_counts_cache, expected_cache)
