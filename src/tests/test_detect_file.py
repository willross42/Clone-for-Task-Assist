from unittest import TestCase
from unittest.mock import patch

from detect import file_ext_test, sniff_contents, detect_filetype
from tests.mocks.response import ResponseMock
from tests.utils import open_test_file


class DetectFileTypeTest(TestCase):
    def setUp(self):
        self.url_csv = "https://www.indiandcold.com/media/photo_export.csv"
        self.csv_file = 'csv_example.csv'
        self.xml_file = 'xml_example.xml'
        self.tsv_file = 'tsv_example.tsv'

    def test_by_filename(self):
        file_type = file_ext_test(self.url_csv)
        self.assertEqual(file_type, "csv")

        file_type = file_ext_test(self.url_xml)
        self.assertEqual(file_type, "xml")

        file_type = file_ext_test(self.url_tsv)
        self.assertEqual(file_type, "tsv")

    def test_by_sniff(self):
        with open_test_file(self.csv_file) as file:
            self.assertEqual(sniff_contents(ResponseMock(fd=file)), "csv")

        with open_test_file(self.tsv_file) as file:
            self.assertEqual(sniff_contents(ResponseMock(fd=file)), "tsv")

        with open_test_file(self.xml_file) as file:
            self.assertEqual(sniff_contents(ResponseMock(fd=file)), "xml")

    def test_by_content_type_header(self):
        headers = {
            'Content-Type': 'text/csv'
        }
        with open_test_file(self.csv_file) as file:
            self.assertEqual(detect_by_content_type(
                ResponseMock(fd=file, headers=headers)), "csv")

        headers = {
            'Content-Type': 'application/xml'
        }
        with open_test_file(self.xml_file) as file:
            self.assertEqual(detect_by_content_type(
                ResponseMock(fd=file, headers=headers)), "xml")

        headers = {
            'Content-Type': 'text/tab-separated-values'
        }
        with open_test_file(self.tsv_file) as file:
            self.assertEqual(detect_by_content_type(
                ResponseMock(fd=file, headers=headers)), "tsv")

    def test_all_flow(self):
        headers = {
            'Content-Type': 'text/csv'
        }
        with patch('requests.get') as mock:
            with open_test_file(self.csv_file) as file:
                mock.return_value = ResponseMock(fd=file, headers=headers)
                self.assertEqual(detect_filetype(self.url_csv), "csv")
