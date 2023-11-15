from app.models import CompilerReport, InvokerReport
from django.test import TestCase
from unittest.mock import patch
from datetime import timedelta


class CompilerReportTestCase(TestCase):
    def setUp(self):
        invoker_report = InvokerReport.objects.create()
        CompilerReport.objects.create(status=CompilerReport.Status.OK, time=timedelta(microseconds=1), invoker_report=invoker_report)
        CompilerReport.objects.create(status=CompilerReport.Status.COMPILER_ERROR, error="Test", time=timedelta(microseconds=1), invoker_report=invoker_report)
        CompilerReport.objects.create(status=CompilerReport.Status.COMPILATION_ERROR, error="Test", time=timedelta(microseconds=1), invoker_report=invoker_report)
        CompilerReport.objects.create(status=CompilerReport.Status.TIMELIMIT, error="Test", time=timedelta(microseconds=1), invoker_report=invoker_report)

    def test_str(self):
        ok = CompilerReport.objects.get(status=CompilerReport.Status.OK)
        compiler_error = CompilerReport.objects.get(status=CompilerReport.Status.COMPILER_ERROR)
        compilation_error = CompilerReport.objects.get(status=CompilerReport.Status.COMPILATION_ERROR)
        timelimit_error = CompilerReport.objects.get(status=CompilerReport.Status.TIMELIMIT)

        self.assertEquals(str(ok), f"{ok.id} - {ok.get_status_display()}")
        self.assertEquals(str(compiler_error), f"{compiler_error.id} - {compiler_error.get_status_display()} | {compiler_error.error}")
        self.assertEquals(str(compilation_error), f"{compilation_error.id} - {compilation_error.get_status_display()} | {compilation_error.error}")
        self.assertEquals(str(timelimit_error), f"{timelimit_error.id} - {timelimit_error.get_status_display()} | {timelimit_error.error}")

    def test_has_error(self):
        ok = CompilerReport.objects.get(status=CompilerReport.Status.OK)
        compiler_error = CompilerReport.objects.get(status=CompilerReport.Status.COMPILER_ERROR)
        compilation_error = CompilerReport.objects.get(status=CompilerReport.Status.COMPILATION_ERROR)
        timelimit_error = CompilerReport.objects.get(status=CompilerReport.Status.TIMELIMIT)

        self.assert_(not ok.has_error())
        self.assert_(compiler_error.has_error())
        self.assert_(compilation_error.has_error())
        self.assert_(timelimit_error.has_error())
