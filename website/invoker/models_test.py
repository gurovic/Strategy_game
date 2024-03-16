from django.core.files import File as FileDjango
from django.utils import timezone
from django.test import TestCase

from invoker.models import InvokerReport, File
import psycopg2


class TestInvokerReport(TestCase):
    def setUp(self):
        InvokerReport.objects.all().delete()
        InvokerReport.objects.create(command="Ok", status=InvokerReport.Status.OK, time_start=timezone.now(),
                                     time_end=timezone.now(), exit_code=0)
        InvokerReport.objects.create(command="RE", status=InvokerReport.Status.RE, time_start=timezone.now(),
                                     time_end=timezone.now(), exit_code=0)
        InvokerReport.objects.create(command="TL", status=InvokerReport.Status.TL, time_start=timezone.now(),
                                     time_end=timezone.now(), exit_code=0)

    def test_str(self):
        ok = InvokerReport.objects.get(status=InvokerReport.Status.OK)
        re = InvokerReport.objects.get(status=InvokerReport.Status.RE)
        tl = InvokerReport.objects.get(status=InvokerReport.Status.TL)

        self.assertEquals(str(ok), '"Ok" - Ok')
        self.assertEquals(str(re), '"RE" - Re')
        self.assertEquals(str(tl), '"TL" - Tl')

    def test_has_error(self):
        ok = InvokerReport.objects.get(status=InvokerReport.Status.OK)
        re = InvokerReport.objects.get(status=InvokerReport.Status.RE)
        tl = InvokerReport.objects.get(status=InvokerReport.Status.TL)

        self.assert_(not ok.has_error())
        self.assert_(re.has_error())
        self.assert_(tl.has_error())


class TestFile(TestCase):
    def setUp(self):
        File.objects.create(file=FileDjango(open(__file__, "r"), name="test"), name="test")

    def tearDown(self):
        for file in File.objects.all():
            file.file.delete()

    def test_str(self):
        file = File.objects.first()

        self.assertEquals(str(file), file.name)
