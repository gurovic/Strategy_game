from django.test import TestCase
from unittest.mock import patch, Mock

from app.compiler import NotSupportedLanguage, CompilerReport, DoNothingCompile, CPPCompile, Compiler, AbstractCompile
from invoker.filesystem import File

import datetime


class TestNotSupportedLanguage(TestCase):
    def test_str(self):
        exception = NotSupportedLanguage("py")
        self.assertEquals(str(exception), "Language py is not supported!")


class TestAbstractCompile(TestCase):
    class CompileTest(AbstractCompile):
        def command(self):
            return "test", "test", "test"

    @patch("app.compiler.InvokerMultiRequestPriorityQueue")
    def test_compile(self, mock_queue: Mock):
        compiler = self.CompileTest("test", "test")
        compiler.compile()
        mock_queue = mock_queue()
        mock_queue.add.assert_called()

    @patch("app.compiler.AbstractCompile.send_report")
    @patch("app.compiler.AbstractCompile.make_report")
    def test_notify(self, mock_make_report: Mock, mock_send_report: Mock):
        report = Mock()
        compiler = self.CompileTest("test", lang="py")
        compiler.notify([report])

        mock_make_report.assert_called_with(report)
        mock_send_report.assert_called()

    @patch("app.models.compiler_report.CompilerReport.objects.create")
    def test_make_report(self, mock_compiler_report: Mock):
        mock = Mock()
        mock.time_start = datetime.datetime.now()
        mock.time_end = datetime.datetime.now()

        compiler = self.CompileTest("test", lang="py")
        compiler.make_report(mock)

        mock_compiler_report.assert_called_once_with(invoker_report=mock, time=mock.time_end - mock.time_start,
                                                     status=CompilerReport.Status.COMPILATION_ERROR, error=mock.error,
                                                     compiled_file=mock.preserved_files.get().file)

    @patch("app.models.compiler_report.CompilerReport")
    def test_send_report(self, mock_compiler_report: Mock):
        mock = Mock()
        compiler = self.CompileTest("test", lang="py", callback=mock)
        compiler.send_report(mock_compiler_report)

        mock.assert_called()


class TestDoNothingCompile(TestCase):

    @patch("app.models.compiler_report.CompilerReport.objects.create")
    def test_compile(self, mock_compiler_report: Mock):
        mock = Mock()
        compiler = DoNothingCompile("test", lang="py", callback=mock)
        compiler.compile()

        mock.assert_called_once_with(mock_compiler_report())


class TestCPPCompile(TestCase):
    def test_command(self):
        compiler = CPPCompile("test", lang="py")
        command, input_file, output_file = compiler.command()

        self.assertEquals(command, "g++ -o compiled main.cpp")
        self.assertEquals(input_file, File("main.cpp", "test"))
        self.assertEquals(output_file, "compiled")


class TestCompiler(TestCase):
    def test_language(self):
        unsupported_languages = []

        for language in Compiler.COMMANDS:
            try:
                Compiler("test", lang=language)
            except NotSupportedLanguage:
                unsupported_languages.append(language)

        if unsupported_languages:
            self.fail(f"Languages {', '.join(unsupported_languages)} is unsupported but should be")

    def test_unsupported_language(self):
        with self.assertRaises(NotSupportedLanguage):
            Compiler("test", lang="test")

    def test_compile(self):
        compiler = Compiler("test", lang="py")
        compiler.command = Mock()
        compiler.compile()

        compiler.command.compile.assert_called_once()

    @patch("invoker.models.InvokerReport")
    def test_notify(self, mock_invoker_report : Mock):
        mock = Mock()
        invoker_request = Compiler("test", lang="py", callback=mock)
        invoker_request.notify(mock_invoker_report)

        mock.assert_called()
