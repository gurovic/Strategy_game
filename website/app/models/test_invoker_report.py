import django.test
from app.models.invoker_report import *


class TestInvokerReport(django.test.TestCase):

    def test_origin(self):
        a = InvokerReport()
        self.assertEqual(a.invoker_id, -1)
        self.assertEqual(a.program_type, '')
        self.assertEqual(a.running_file, None)
        self.assertEqual(a.time_start, None)
        self.assertEqual(a.time_end, None)
        self.assertEqual(a.program_status, STATUS["NS"])
        self.assertEqual(a.program_error_text, None)
