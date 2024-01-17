from unittest.mock import patch, Mock

from django.test import TestCase

from .sandbox_notify_receiver import SandboxNotifyReceiver


class TestSandboxNotifyReceiver(TestCase):
    @patch('app.classes.sandbox_notify_receiver.Sandbox')
    def test_create(self, mock_sandbox):
        mock_sandbox_instance = Mock()
        mock_sandbox.return_value = mock_sandbox_instance

        sandbox = SandboxNotifyReceiver(None, None)
        self.assertEqual(sandbox.report, None)
        self.assertEqual(sandbox.strategy, None)

    @patch('app.classes.sandbox_notify_receiver.Sandbox')
    def test_run(self, mock_sandbox):
        mock_sandbox_instance = Mock()
        mock_sandbox.return_value = mock_sandbox_instance

        class MockSandbox:
            count = 0

            def run_battle(self):
                self.count += 1

        sandbox = SandboxNotifyReceiver(None, None)
        sandbox.sandbox = MockSandbox()
        sandbox.run()
        self.assertEqual(sandbox.sandbox.count, 1)

    @patch('app.classes.sandbox_notify_receiver.Sandbox')
    def test_notify(self, mock_sandbox):
        mock_sandbox_instance = Mock()
        mock_sandbox.return_value = mock_sandbox_instance

        report = 'done'
        sandbox = SandboxNotifyReceiver(None, None)
        sandbox.notify(report)
        self.assertEqual(sandbox.report, report)
