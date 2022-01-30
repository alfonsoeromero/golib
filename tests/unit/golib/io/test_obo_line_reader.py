from unittest import TestCase

from golib.io.obo_line_reader import OboLineReader

from tests.common.obo_line_reader_fixture import OboLineReaderFixture


class TestOboLineReader(TestCase):
    def setUp(self) -> None:
        self._fixture = OboLineReaderFixture()

    def test_should_read_expected_lines_from_empty_file(self):
        # arrange
        file_name = self._fixture.empty_file
        sut = OboLineReader(file_name)
        expected_num_lines = self._fixture.expected_num_lines_empty_file()
        expected_lines = self._fixture.expected_lines_empty_file()

        # act
        actual_lines = [x for x in sut]

        # assert
        self.assertEqual(len(actual_lines), expected_num_lines)
        self.assertListEqual(expected_lines, actual_lines)

    def test_should_read_expected_lines_from_comments_and_empty_file(self):
        # arrange
        file_name = self._fixture.comments_and_empty_lines
        sut = OboLineReader(file_name)
        expected_num_lines = self._fixture.\
            expected_num_lines_comments_and_empty_lines()
        expected_lines = self._fixture.\
            expected_lines_comments_and_empty_lines()

        # act
        actual_lines = [x for x in sut]

        # assert
        self.assertEqual(len(actual_lines), expected_num_lines)
        self.assertListEqual(expected_lines, actual_lines)

    def test_should_read_expected_lines_from_filled_file(self):
        # arrange
        file_name = self._fixture.filled_file
        sut = OboLineReader(file_name)
        expected_num_lines = self._fixture.\
            expected_num_lines_filled_file()
        expected_lines = self._fixture.\
            expected_lines_filled_file()

        # act
        actual_lines = [x for x in sut]

        # assert
        self.assertEqual(len(actual_lines), expected_num_lines)
        self.assertListEqual(expected_lines, actual_lines)
