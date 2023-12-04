from django.test import TestCase
from unittest.mock import patch


class IntegrationTest(TestCase):
    @patch("File")
    @patch("FileLoader")
    def test_upload(self, File):

        pass

    def test_creating_battle(self):
        pass

    def test_run(self):
        pass

    def test_create_response(self):
        pass

    def test_response_in_views(self):
        pass
