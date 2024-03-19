import time
import os

from django.test import TestCase
from django.conf import settings

from app.compiler import Compiler, CompilerReport
from app.launcher import Launcher
from .invoker import Invoker, NormalProcess


class TestInvokerSystem(TestCase):
    def test(self):
        for lang in settings.SUPPORTED_LANGUAGES:
            file = os.path.abspath('invoker/invoker_system_integration_test/invoker_integration.{}'.format(lang))

            self.launch_call = False
            self.compiler_call = False

            def get_launcher_callback(process: NormalProcess):
                self.launch_call = True
                process_output = process.connect(input_data="Hello")
                self.assertEqual(process_output, "5879349 Hello\n")

            def get_compiler_callback(report: CompilerReport):
                self.compiler_call = True
                compiled_file = report.compiled_file.path
                launcher = Launcher(compiled_file, get_launcher_callback)
                launcher.launch()

            compiler = Compiler(file, lang, get_compiler_callback)
            compiler.compile()

            counter = time.perf_counter()
            while ((time.perf_counter() - counter) < 14) & ((self.launch_call & self.compiler_call) == False):
                pass
            self.assertEqual(self.compiler_call, True, "language: {} is not compiling".format(lang))
            self.assertEqual(self.launch_call, True, "language: {} is not launching".format(lang))
