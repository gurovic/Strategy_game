from app.classes import Sandbox, Battle

from django.test import TestCase


class SandboxTest(TestCase):
    def test_create(self):
        a = Sandbox(None, None)
        self.assertEqual(a.game, None)
        self.assertEqual(a.strategy, None)
        self.assertEqual(type(a.battle), Battle)

    def test_get_report(self):
        a = Sandbox(None, None)

    def test_run_battle(self):
        pass
