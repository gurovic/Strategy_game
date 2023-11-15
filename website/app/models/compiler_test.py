from django.test import TestCase
from app.models import CompilerReport


class CompilerReportTestCase(TestCase):
    def setUp(self):
        CompilerReport.objects.create(status=CompilerReport.Status.OK)
        CompilerReport.objects.create(status=CompilerReport.Status.COMPILER_ERROR, error="Test")
        CompilerReport.objects.create(status=CompilerReport.Status.COMPILATION_ERROR, error="Test")
        CompilerReport.objects.create(status=CompilerReport.Status.TIMELIMIT, error="Test")

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

        self.assert_(ok.has_error())
        self.assert_(not compiler_error.has_error())
        self.assert_(not compilation_error.has_error())
        self.assert_(not timelimit_error.has_error())
