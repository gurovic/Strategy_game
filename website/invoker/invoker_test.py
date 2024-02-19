from unittest.mock import patch, Mock
from django.test import TestCase

from invoker.invoker import Invoker, NoInvokerPoolCallbackData
from invoker.models import InvokerReport
from invoker.filesystem import File


class TestInvoker(TestCase):
    @patch("invoker.filesystem.File.load")
    def test_run(self, mock_file_load: Mock):
        mock_environment = Mock()
        mock_invoker_run_callback = Mock()

        invoker = Invoker()
        invoker.environment = mock_environment

        invoker.run("echo Hello World", files=["test", File("test_file", "test")], preserve_files=["test"],
                    timelimit=10, label="test", callback=mock_invoker_run_callback)

        self.assertEqual(invoker._callback, mock_invoker_run_callback)
        mock_file_load.assert_called_with("test")
        mock_environment.assert_called_once_with(invoker.notify)
        mock_environment().launch.assert_called_once_with('echo Hello World', file_system=[mock_file_load("test"), File(name='test_file', source='test')],
                                                          preserve_files=['test'], timelimit=10, label="test")

    @patch("invoker.invoker.Invoker.free")
    @patch("invoker.invoker.Invoker.send_report")
    @patch("invoker.invoker.Invoker.make_report")
    def test_notify(self, mock_make_report: Mock, mock_send_report: Mock, mock_free: Mock):
        mock_result = Mock()

        invoker = Invoker()
        invoker.notify(mock_result)

        mock_make_report.assert_called_once_with(mock_result)
        mock_send_report.assert_called_once_with(mock_make_report())
        mock_free.assert_called_once()

    def test_free(self):
        mock_callback = Mock()
        invoker = Invoker()
        invoker.callback_free_myself = mock_callback

        invoker.free()

        mock_callback.assert_called_once_with(invoker)

    def test_free_error(self):
        invoker = Invoker()

        self.assertRaises(NoInvokerPoolCallbackData, invoker.free)

    @patch("invoker.models.File.objects.create")
    @patch("invoker.models.InvokerReport.objects.create")
    def test_make_report(self, mock_report_create: Mock, mock_file: Mock):
        mock_result = Mock()
        mock_result.input_files = [File("file1", "test")]
        mock_result.preserved_files = [File("file2", "test")]

        invoker = Invoker()
        report: Mock = invoker.make_report(mock_result)

        mock_report_create.assert_called_once_with(command=mock_result.command, time_start=mock_result.time_start,
                                                    time_end=mock_result.time_end, exit_code=mock_result.exit_code,
                                                    output=mock_result.output, status=InvokerReport.Status.TL)
        report.input_files.add.assert_called_once_with(mock_file())
        report.preserved_files.add.assert_called_once_with(mock_file())
        report.save.assert_called()

    def test_send_report(self):
        mock_report = Mock()

        mock_callback = Mock()
        invoker = Invoker()
        invoker._callback = mock_callback

        invoker.send_report(mock_report)
        mock_callback.assert_called_once_with(mock_report)
