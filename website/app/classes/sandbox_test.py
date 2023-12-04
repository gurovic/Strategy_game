from app.classes.sandbox import Sandbox
from unittest.mock import Mock,patch

from django.test import TestCase


class SandboxTest(TestCase):
    @patch("app.models.Battle")
    def test_create(self, mock_battle):
        a =

    def test_running(self):
        pass

    def test_get_result(self):
        pass
