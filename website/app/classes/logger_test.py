import unittest
from logger import class_log
import os

class TestLoggerMethods(unittest.TestCase):
    @class_log
    class InnerClass:
        def __init__(self):
            pass

        def method1(self, arg1, arg2):
            return arg1 + arg2

        def method2(self, arg):
            if arg == 0:
                raise ValueError("Argument cannot be zero")
            return 10 / arg

    def test_method1(self):
        test_instance = self.InnerClass()
        result = test_instance.method1(5, 3)
        self.assertEqual(result, 8)

    def test_method2(self):
        test_instance = self.InnerClass()
        with self.assertRaises(ValueError):
            test_instance.method2(0)

    @classmethod
    def tearDownClass(cls):
        logs_file_path = os.path.join(os.path.dirname(__file__), '../../media/logs.txt')
        os.remove(logs_file_path)