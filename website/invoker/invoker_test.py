from django.test import TestCase
from unittest.mock import patch, Mock

from invoker.invoker import Invoker


class TestInvoker(TestCase):
    @patch("invoker.models.InvokerReport")
    def test_notify(self, mock_invoker_report : Mock):
        mock = Mock()
        invoker = Invoker()
        invoker.run("echo Hello World", callback=mock)
        mock.assert_called()
