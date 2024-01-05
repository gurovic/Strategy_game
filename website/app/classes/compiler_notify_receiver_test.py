from django.test import TestCase

from .compiler_notify_receiver import CompilerNotifyReceiver


class TestCompilerNotifyReceiver(TestCase):
    def test_lang(self):
        langs = ['c++', 'python']
        res = ['cpp', 'py']
        for i in range(len(langs)):
            file = CompilerNotifyReceiver(None, langs[i])
            self.assertEqual(file.lang, res[i])

    def test_run(self):
        class MockCompiler:
            count = 0

            def compile(self):
                self.count += 1

        a = CompilerNotifyReceiver(None, 'c++')
        a.compiler = MockCompiler()
        a.run()
        self.assertEqual(a.compiler.count, 1)

    def test_notify(self):
        report = 'done'
        a = CompilerNotifyReceiver(None, 'c++')
        a.notify(report)
        self.assertEqual(a.report, report)
