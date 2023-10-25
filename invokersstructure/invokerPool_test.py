import unittest
from invokerPool import InvokerPool

class TestInvokerPool(unittest.testCase):
    def test_count(self):
        in_p = InvokerPool
        self.assertEqual(in_p.ALL_INVOKERS_COUNT,100)
    def test_function(self):
        pass