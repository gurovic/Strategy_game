import datetime
#
from django.test import TestCase
from unittest.mock import patch, Mock

from app.launcher import Launcher


class TestLauncher(TestCase):
    class LaunchTest(Launcher):
        pass

    @patch("app.launcher.InvokerMultiRequestPriorityQueue")
    def test_launch(self, mock_queue: Mock):
        launcher = self.LaunchTest(".!.@,#,$.%,^./file.epy")
        launcher.launch()
        mock_queue = mock_queue()
        mock_queue.add.assert_called()

    def test_notify(self):
        callback = Mock()
        report = Mock()
        launcher = self.LaunchTest(".!.@,#,$.%,^./file.epy", callback=callback)
        launcher.notify([report])

        callback.assert_called_once_with([report])

    def test_CPP_launch(self):
        launcher = self.LaunchTest("compiled.ecpp")
        command = launcher.command()
        self.assertEquals(command, "compiled.ecpp")

    def test_PYTHON_launch(self):
        launcher = self.LaunchTest("compiled.epy")
        command = launcher.command()
        self.assertEquals(command, "python3 compiled.epy")
