import subprocess

from unittest.mock import patch, Mock
from django.test import TestCase

from invoker.invoker import Invoker, NoInvokerPoolCallbackData, InvokerProcess, TimeoutExpired, NormalProcess, BufferWrapper
from invoker.models import InvokerReport
from invoker.filesystem import File


class TestInvokerProcess(TestCase):
    class InvokerProcessTest(InvokerProcess):
        def wait(self):
            pass

        def kill(self):
            pass

    @patch("invoker.invoker.InvokerProcess.register_callback")
    def test_init(self, mock_register: Mock):
        mock_callback = Mock()

        self.InvokerProcessTest("test", 10, mock_callback)
        mock_register.assert_called_once()

    @patch("invoker.invoker.Thread")
    def test_register_callback(self, mock_thread: Mock):
        process = self.InvokerProcessTest()
        process.register_callback()
        mock_thread.assert_called_once_with(target=process._wait_for_end)
        mock_thread().start.assert_called_once()

    def test_connect(self):
        process = self.InvokerProcessTest()
        process.stdin = Mock()
        process.stdout = Mock()

        process.connect("test")

        process.stdin.write.assert_called_once_with("test\n")
        process.stdout.readline.assert_called_once()

    def test_wait_for_end(self):
        process = self.InvokerProcessTest(timelimit=10)
        process.wait = Mock(side_effect=TimeoutExpired(10))
        process.kill = Mock()
        process.send_callback = Mock()

        process._wait_for_end()

        process.wait.assert_called_once()
        process.kill.assert_called_once()
        process.send_callback.assert_called_once()

    def test_send_callback(self):
        process = self.InvokerProcessTest()
        process.callback = Mock()

        process.send_callback()

        process.callback.assert_called_once_with(False)


class TestNormalProcess(TestCase):
    def test_init(self):
        mock_process = Mock()
        process = NormalProcess(mock_process)

        self.assertEqual(process.stdin, mock_process.stdin)
        self.assertEqual(process.stdout, BufferWrapper(mock_process.stdout))

    def test_wait(self):
        mock_process = Mock()
        mock_process.wait = Mock(side_effect=subprocess.TimeoutExpired("test", 10))

        process = NormalProcess(mock_process, timelimit=10)
        self.assertRaises(TimeoutExpired, process.wait)

        mock_process.wait.assert_called_once_with(10)

    def test_kill(self):
        mock_process = Mock()
        process = NormalProcess(mock_process)
        process.kill()

        mock_process.kill.assert_called_once()


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

    def test_notify(self):
        mock_result = Mock()

        invoker = Invoker()

        invoker.make_report = Mock()
        invoker.send_report = Mock()
        invoker.free = Mock()

        invoker.notify(mock_result)

        invoker.make_report.assert_called_once_with(mock_result)
        invoker.send_report.assert_called_once_with(invoker.make_report())
        invoker.free.assert_called_once()

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
                                                    output=mock_result.output, error=mock_result.error, status=InvokerReport.Status.TL)
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
