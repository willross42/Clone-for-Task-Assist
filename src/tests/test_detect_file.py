from unittest import TestCase
from unittest.mock import patch

from src.detect import by_file_name, by_content_type, by_sniff_contents, detect_filetype
from src.tests.mocks.response import ResponseMock
from src.tests.utils import open_test_file


class DetectFileTypeTest(TestCase):
    def setUp(self):
        self.url_csv = "https://www.indiandcold.com/media/photo_export.csv"
        self.csv_file = 'csv_example.csv'
        self.url_xml = "https://factionskis.com/pages/photoslurp-product-feed"
        self.xml_file = 'xml_example.xml'
        self.url_tsv = "http://commondatastorage.googleapis.com/newfeedspec/example_feed_txt.zip"
        self.tsv_file = 'tsv_example.tsv'

    def test_by_filename(self):
        file_type = by_file_name(self.url_csv)
        self.assertEqual(file_type, "csv")

        file_type = by_file_name(self.xml_file)
        self.assertEqual(file_type, "xml")

        file_type = by_file_name(self.tsv_file)
        self.assertEqual(file_type, "tsv")


    def test_by_content_type_header(self):
        headers = {
            'Content-Type': 'text/csv'
        }
        with open_test_file(self.csv_file) as file:
            self.assertEqual(by_content_type(
                ResponseMock(fd=file, headers=headers)), "csv")

        headers = {
            'Content-Type': 'application/xml'
        }
        with open_test_file(self.xml_file) as file:
            self.assertEqual(by_content_type(
                ResponseMock(fd=file, headers=headers)), "xml")

        headers = {
            'Content-Type': 'text/tab-separated-values'
        }
        with open_test_file(self.tsv_file) as file:
            self.assertEqual(by_content_type(
                ResponseMock(fd=file, headers=headers)), "tsv")


    def test_by_sniff_contents(self):
        with open_test_file(self.csv_file) as file:
            self.assertEqual(by_sniff_contents(ResponseMock(fd=file)), "csv")

        with open_test_file(self.xml_file) as file:
            self.assertEqual(by_sniff_contents(ResponseMock(fd=file)), "xml")

        with open_test_file(self.tsv_file) as file:
            self.assertEqual(by_sniff_contents(ResponseMock(fd=file)), "tsv")


    def test_all_flow(self):
        headers = {
            'Content-Type': 'text/csv'
        }
        with patch('requests.get') as mock:
            with open_test_file(self.csv_file) as file:
                mock.return_value = ResponseMock(fd=file, headers=headers)
                self.assertEqual(detect_filetype(self.url_csv), "csv")

        headers = {
            'Content-Type': 'application/xml'
        }
        with patch('requests.get') as mock:
            with open_test_file(self.xml_file) as file:
                mock.return_value = ResponseMock(fd=file, headers=headers)
                self.assertEqual(detect_filetype(self.url_xml), "xml")

        headers = {
            'Content-Type': 'text/tab-separated-values'
        }
        with patch('requests.get') as mock:
            with open_test_file(self.tsv_file) as file:
                mock.return_value = ResponseMock(fd=file, headers=headers)
                self.assertEqual(detect_filetype(self.url_tsv), "tsv")
