from unittest.mock import patch, Mock

from django.test import TestCase

from .sandbox_notify_receiver import SandboxNotifyReceiver


class TestSandboxNotifyReceiver(TestCase):
    @patch('app.classes.sandbox_notify_receiver.Sandbox')
    def test_create(self, sandbox_mock):
        mock_compiler_instance = Mock()
        sandbox_mock.return_value = mock_compiler_instance

        a = SandboxNotifyReceiver(None, None)
        self.assertEqual(a.report, None)
        self.assertEqual(a.game, None)
        self.assertEqual(a.strategy, None)

    @patch('app.classes.sandbox_notify_receiver.Sandbox')
    def test_run(self, sandbox_mock):
        mock_compiler_instance = Mock()
        sandbox_mock.return_value = mock_compiler_instance

        class MockSandbox:
            count = 0

            def run_battle(self):
                self.count += 1

        a = SandboxNotifyReceiver(None, None)
        a.sandbox = MockSandbox()
        a.run()
        self.assertEqual(a.sandbox.count, 1)

    @patch('app.classes.sandbox_notify_receiver.Sandbox')
    def test_notify(self, sandbox_mock):
        mock_compiler_instance = Mock()
        sandbox_mock.return_value = mock_compiler_instance

        report = 'done'
        a = SandboxNotifyReceiver(None, None)
        a.notify(report)
        self.assertEqual(a.report, report)
