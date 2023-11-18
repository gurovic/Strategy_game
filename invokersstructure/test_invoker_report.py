import django.test
from invoker_report import *


class TestInvokerReport(django.test.TestCase):
    def test_different(self):
        a = InvokerReport
        b = InvokerReport
        self.assertEqual(a, b)

    def test_origin(self):
        a = InvokerReport
        self.assertEqual(a.invoker_id, -1)
        self.assertEqual(a.program_type, '')
        self.assertEqual(a.running_file, None)
        self.assertEqual(a.time_start, None)
        self.assertEqual(a.time_end, None)
        self.assertEqual(a.program_status, STATUS["NS"])
        self.assertEqual(a.program_error_text, None)
