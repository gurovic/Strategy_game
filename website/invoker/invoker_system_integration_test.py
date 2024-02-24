import os
from unittest.mock import patch, Mock
from django.test import TestCase

from app.compiler import Compiler
from app.launcher import Launcher
from .invoker import Invoker
from .invoker_request import InvokerRequest
from .models import InvokerReport
from .invoker_multi_request import InvokerMultiRequest, Priority
from .invoker_multi_request_priority_queue import InvokerMultiRequestPriorityQueue


class TestInvokerSystem(TestCase):
    def test(self):
        compiler_callback = Mock()
        launcher_callback = Mock()

        file = os.path.abspath('invoker/test_solutions/solution1.py')

        compiler = Compiler(file, 'py', compiler_callback)
        compiler.compile()

        compiler_callback.assert_called()
        #compiled_file = compiler_callback.call_args[0].compiled_file
        compiled_file = compiler.compiler.output_file

        launcher = Launcher(compiled_file, launcher_callback)
        launcher.launch()

        launcher_callback.assert_called()
