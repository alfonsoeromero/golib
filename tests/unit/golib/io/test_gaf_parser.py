from unittest import TestCase
from go_lib.io.gaf_parser import GafParser

from tests.common.gaf_parser_fixture import GafParserFixture


class TestGafParser(TestCase):
    def setUp(self) -> None:
        self._fixture = GafParserFixture()

    def test_should_read_correct_headers_from_file_with_no_annotations(self):
        # arrange
        expected_header_keys = self._fixture.expected_header_keys()
        expected_header_values = self._fixture.expected_num_header_values()

        # act
        sut = GafParser(self._fixture.gaf_file_only_header)
        _ = [x for x in sut]
        actual_header_keys = list(sut.headers.keys())
        actual_header_values = len(sut.headers.values())

        # assert
        self.assertListEqual(expected_header_keys, actual_header_keys)
        self.assertEqual(actual_header_values, expected_header_values)

    def test_should_read_correct_count_from_full_file(self):
        # arrange
        expected_header_keys = self._fixture.expected_header_keys()
        expected_header_values = self._fixture.expected_num_header_values()
        expected_num_annotations = self._fixture.expected_num_annotations()
        exoected_num_unique_go_terms = self._fixture.expected_num_unique_go_terms()
        expected_unique_e_codes = self._fixture.expected_unique_evidence_codes()

        # act
        sut = GafParser(self._fixture.gaf_file)
        annotations = [x for x in sut]
        go_terms = set(x.go_id for x in annotations)
        evidence_codes = sorted(list(set(x.evidence_code for x in annotations)))
        actual_header_keys = list(sut.headers.keys())
        actual_header_values = len(sut.headers.values())
        actual_num_annotations = len(annotations)
        actual_num_unique_go_terms = len(go_terms)

        # assert
        self.assertListEqual(expected_header_keys, actual_header_keys)
        self.assertListEqual(evidence_codes, expected_unique_e_codes)
        self.assertEqual(actual_header_values, expected_header_values)
        self.assertEqual(actual_num_annotations, expected_num_annotations)
        self.assertEqual(actual_num_unique_go_terms, exoected_num_unique_go_terms)
