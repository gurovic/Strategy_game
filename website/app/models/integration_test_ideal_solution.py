from django.test import TestCase
from unittest.mock import patch


class IntegrationTest(TestCase):
    @patch("File")
    @patch("FileLoader")
    def test_upload(self, file, fileloader):
        report = fileloader(file)
        TestCase.assertEqual(report.compiler_report.status, "OK", "Failed")

    @patch("Battle")
    def test_creating_battle(self, battle):
        pass

    def test_run(self):
        pass

    def test_create_response(self):
        pass

    def test_response_in_views(self):
        pass
