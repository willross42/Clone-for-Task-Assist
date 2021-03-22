from unittest import mock, TestCase
import requests
import csv
from detect import file_ext_test, sniff_contents, detect_filetype


class DetectFileTypeTest(TestCase):
    def setUp(self):
        self.url = "https://www.indiandcold.com/media/photo_export.csv"
        self.content = open('csv_example.csv', encoding='utf8').read()

    def tearDown(self) -> None:
        pass

    def test_by_filename(self):
        file_type = file_ext_test(self.url)
        self.assertEqual(file_type, "csv")

    def test_all_flow(self):
        with mock.patch('requests.get') as mock_request:
            mock_request.return_value.status_code = 200
            mock_request.return_value = self.content

            #with requests.get(self.url, allow_redirects=True, stream=True) as response:

            file_type = detect_filetype(self.url)

            self.assertEqual(file_type, "csv")