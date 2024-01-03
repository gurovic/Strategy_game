import time

from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import Mock, patch

from .classes_for_sanbox_views import CompilerNotifyReceiver, SandboxNotifyReceiver


class TestCreateSandbox(TestCase):
    pass


class TestCompilerNotifyReceiver(TestCase):
    def setUp(self):
        pass

    def test_lang(self):
        langs = ['c++', 'java', 'python', 'javascript', 'c#', 'c']
        res = ['cpp', 'Java', 'py', 'js', 'cs', 'c']
        for i in range(len(langs)):
            file = CompilerNotifyReceiver(None, langs[i])
            self.assertEqual(file.lang, res[i])

    @patch('app.views.sandbox_views.CompileFile.compiler')
    def test_run(self):
        pass

    def test_notify(self):
        pass
