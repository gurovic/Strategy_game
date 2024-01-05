from django.test import TestCase

from .sandbox_notify_receiver import SandboxNotifyReceiver


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
