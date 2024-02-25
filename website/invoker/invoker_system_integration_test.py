from unittest.mock import patch, Mock
from django.test import TestCase

from app.compiler import Compiler
from app.launcher import Launcher
from .invoker import Invoker, NormalProcess


class TestInvokerSystem(TestCase):
    def test(self):
        compiler_callback = Mock()
        launcher_callback = Mock()

        file = 'invoker/test_solutions/solution1.py'

        compiler = Compiler(file, 'py', compiler_callback)
        compiler.compile()

        compiler_callback.assert_called()
        compiler_report = compiler_callback.call_args.args[0]
        compiled_file = compiler_report.compiled_file
        path_to_compiled_file = compiled_file.path

        launcher = Launcher(path_to_compiled_file, launcher_callback)
        launcher.launch()

        launcher_callback.assert_called()
        process = launcher_callback.call_args.args[0]

        self.assertEqual(type(process), NormalProcess)
