from unittest import TestCase
from golib.io.obo_parser import OboParser

from tests.common.obo_parser_fixture import OboParserFixture


class TestOboParser(TestCase):
    def setUp(self) -> None:
        self._fixture = OboParserFixture()

    def test_should_read_correct_headers_from_file_with_no_stanzas(self):
        # arrange
        expected_header_keys = self._fixture.expected_headers_keys()
        expected_header_values = self._fixture.expected_num_header_values()

        # act
        sut = OboParser(self._fixture.obo_file_only_header)
        _ = [x for x in sut]
        actual_header_keys = list(sut.headers.keys())
        actual_header_values = sum(len(v) for v in sut.headers.values())

        # assert
        self.assertListEqual(expected_header_keys, actual_header_keys)
        self.assertEqual(actual_header_values, expected_header_values)

    def test_should_read_correct_count_from_full_file(self):
        # arrange
        expected_header_keys = self._fixture.expected_headers_keys()
        expected_header_values = self._fixture.expected_num_header_values()
        expected_num_stanzas = self._fixture.expected_num_stanzas()

        # act
        sut = OboParser(self._fixture.obo_file)
        stanzas = [x for x in sut]
        actual_header_keys = list(sut.headers.keys())
        actual_header_values = sum(len(v) for v in sut.headers.values())
        actual_num_stanzas = len(stanzas)

        # assert
        self.assertListEqual(expected_header_keys, actual_header_keys)
        self.assertEqual(actual_header_values, expected_header_values)
        self.assertEqual(actual_num_stanzas, expected_num_stanzas)
