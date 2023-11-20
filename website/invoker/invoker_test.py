from django.test import TestCase
from unittest.mock import patch, Mock

from invoker.invoker import Invoker


class TestInvoker(TestCase):
    @patch("invoker.models.InvokerReport")
    def test_notify(self, mock_invoker_report: Mock):
        mock_invoker_run_callback = Mock()
        mock_callback = Mock()
        invoker = Invoker()
        invoker.callback_free_myself = mock_callback
        invoker.run("echo Hello World", callback=mock_invoker_run_callback)
        mock_invoker_run_callback.assert_called()
