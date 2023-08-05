import unittest
from unittest.mock import patch

from tap_file.tap_object import TapData, TapHeader


class MockStream:
    def __init__(self):
        self.data = None
        self.errors = set()

    def payload(self):
        return self.data, self.errors


class TestTapHeader(unittest.TestCase):

    def setUp(self):
        def dummy_grade(s1, s2, _):
            return s1, s2

        stream = MockStream()
        stream.data = b'\x03\x01\x10\x47\x32TEST            321'
        with patch('tap_file.tap_object.DataStream') as mock_data_stream:
            mock_data_stream.grade_streams = dummy_grade
            self.header = TapHeader(stream, stream)

    def test_htype(self):
        self.assertEqual(str(self.header.htype), 'HeaderType.PRG')

    def test_start(self):
        self.assertEqual(self.header.start, 0x1001)

    def test_end(self):
        self.assertEqual(self.header.end, 0x3247)

    def test_name(self):
        self.assertEqual(self.header.name, b'TEST            ')

    def test_data(self):
        self.assertEqual(self.header.data, b'321')


class TestTapSeq(unittest.TestCase):

    def setUp(self):
        def dummy_grade(s1, s2, _):
            return s1, s2

        stream = MockStream()
        stream.data = b'\x02The quick brown fox jumps over the lazy dog\x00'
        with patch('tap_file.tap_object.DataStream') as mock_data_stream:
            mock_data_stream.grade_streams = dummy_grade
            self.header = TapHeader(stream, stream)

    def test_data(self):
        self.assertTrue(self.header.seq_eof)
        self.assertEqual(self.header.data, b'The quick brown fox jumps over the lazy dog')


class TestTapData(unittest.TestCase):

    def setUp(self):
        def dummy_grade(s1, s2, _):
            return s1, s2

        stream = MockStream()
        stream.data = b'The quick brown fox jumps over the lazy dog\x00'
        with patch('tap_file.tap_object.DataStream') as mock_data_stream:
            mock_data_stream.grade_streams = dummy_grade
            self.header = TapData(stream, stream, len(stream.data))

    def test_data(self):
        self.assertEqual(self.header.data, b'The quick brown fox jumps over the lazy dog\x00')
