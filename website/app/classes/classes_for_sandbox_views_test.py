import time

from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import Mock, patch, MagicMock

from .classes_for_sanbox_views import CompilerNotifyReceiver, SandboxNotifyReceiver


class TestSandboxNotifyReceiver(TestCase):
    def test_create(self):
        class MockGame:
            number_of_players = 0

        a = SandboxNotifyReceiver(MockGame, None)
        self.assertEqual(a.report, None)
        self.assertEqual(a.game, MockGame)
        self.assertEqual(a.strategy, None)

    def test_run(self):
        class MockGame:
            number_of_players = 0

        class MockSandbox:
            count = 0

            def run_battle(self):
                self.count += 1

        a = SandboxNotifyReceiver(MockGame, None)
        a.sandbox = MockSandbox()
        a.run()
        self.assertEqual(a.sandbox.count, 1)

    def test_notify(self):
        class MockGame:
            number_of_players = 0

        report = 'done'
        a = SandboxNotifyReceiver(MockGame, None)
        a.notify(report)
        self.assertEqual(a.report, report)


class TestCompilerNotifyReceiver(TestCase):
    def setUp(self):
        pass

    def test_lang(self):
        langs = ['c++', 'python']
        res = ['cpp', 'py']
        for i in range(len(langs)):
            file = CompilerNotifyReceiver(None, langs[i])
            self.assertEqual(file.lang, res[i])

    def test_run(self):
        class MockCompiler:
            count = 0

            def compile(self):
                self.count += 1

        a = CompilerNotifyReceiver(None, 'c++')
        a.compiler = MockCompiler()
        a.run()
        self.assertEqual(a.compiler.count, 1)

    def test_notify(self):
        report = 'done'
        a = CompilerNotifyReceiver(None, 'c++')
        a.notify(report)
        self.assertEqual(a.report, report)
