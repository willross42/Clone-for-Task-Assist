from unittest import TestCase
from detect import file_ext_test, sniff_contents
from tests.mocks.response import ResponseMock
from tests.utils import open_test_file


class DetectFileTypeTest(TestCase):
    def setUp(self):
        self.url = "https://www.indiandcold.com/media/photo_export.csv"

    def test_by_filename(self):
        file_type = file_ext_test(self.url)
        self.assertEqual(file_type, "csv")

    def test_by_sniff(self):
        with open_test_file('csv_example.csv') as file:
            self.assertEqual(sniff_contents(ResponseMock(fd=file)), "csv")
