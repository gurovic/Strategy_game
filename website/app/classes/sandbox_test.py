from app.classes.sandbox import Sandbox
from unittest.mock import Mock

from django.test import TestCase


class SandboxTest(TestCase):
    def test_create(self):
        a = Sandbox(None, None)
        self.assertEqual(a.game, None)
        self.assertEqual(a.strategy, None)

    def test_get_report(self):
        a = Sandbox(None, None)
        a.battle = Mock()
        a.report = "1"
        self.assertEqual("1", a.get_report())

    def test_run_battle(self):
        pass
