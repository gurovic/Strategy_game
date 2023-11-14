from django.test import TestCase
from app.models import CompilerReport


class CompilerReportTestCase(TestCase):
    def setUp(self):
        CompilerReport.objects.create(status=CompilerReport.Status.OK)
        CompilerReport.objects.create(status=CompilerReport.Status.ERROR, error="Test")

    def test_str(self):
        ok = CompilerReport.objects.get(status=CompilerReport.Status.OK)
        error = CompilerReport.objects.get(status=CompilerReport.Status.ERROR)
        self.assertEquals(str(ok), f"{ok.id} - {ok.get_status_display()}")
        self.assertEquals(str(error), f"{error.id} - {error.get_status_display()} | {error.error}")
