from unittest import TestCase

from golib.io.gaf_line_reader import GafLineReader

from tests.common.gaf_line_reader_fixture import GafLineReaderFixture


class TestGafLineReader(TestCase):
    def setUp(self) -> None:
        self._fixture = GafLineReaderFixture()

    def test_should_read_expected_useful_lines_from_gaf_file(self):
        # arrange
        file_name = self._fixture.gaf_file
        sut = GafLineReader(file_name)
        expected_num_lines = self._fixture.expected_useful_lines_gaf_file()

        # act
        actual_lines = [x for x in sut]

        # assert
        self.assertEqual(len(actual_lines), expected_num_lines)

    def test_should_read_expected_lines_from_empty_file(self):
        # arrange
        file_name = self._fixture.empty_file
        sut = GafLineReader(file_name)
        expected_num_lines = self._fixture.expected_num_lines_empty_file()
        expected_lines = self._fixture.expected_lines_empty_file()

        # act
        actual_lines = [x for x in sut]

        # assert
        self.assertEqual(len(actual_lines), expected_num_lines)
        self.assertListEqual(expected_lines, actual_lines)
