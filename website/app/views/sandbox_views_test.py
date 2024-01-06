from django.test import TestCase
from django.urls import reverse
from django.http import HttpRequest
from django.contrib.auth.models import User
from unittest.mock import Mock, patch

from app.models import CompilerReport, Game
from app.views.sandbox_views import show


class TestSandboxViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.game = Game.objects.create(id=0)
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.compiler_report = CompilerReport.objects.create(
            compiled_file=None,
            status=0,
        )

    def test_views_url_exists(self):
        response = self.client.get('/app/sandbox/0')
        self.assertEqual(response.status_code, 200)

    def test_views_use_correct_template(self):
        response = self.client.get('/app/sandbox/0')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sandbox.html')

    def test_views_use_correct_context(self):
        response = self.client.get('/app/sandbox/0')
        self.assertEqual(response.status_code, 200)

    @patch('app.views.sandbox_views.CompilerNotifyReceiver')
    def test_post_compiler_request(self, MockCompilerNotifyReceiver):
        mock_compiler_instance = Mock()
        MockCompilerNotifyReceiver.return_value = mock_compiler_instance

        request = Mock()
        request.method = 'POST'
        request.POST = {'type': 'compiler', 'language': 'python'}
        request.FILES = {'strategy': Mock()}

        response = show(request, self.game.pk)

        mock_compiler_instance.run.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, 'sandbox.html')
        self.assertEqual(response.context['status'], 'receive compiler report')

    @patch('app.views.sandbox_views.SandboxNotifyReceiver')
    def test_post_sandbox_request(self, MockSandboxNotifyReceiver):
        mock_sandbox_instance = Mock()
        MockSandboxNotifyReceiver.return_value = mock_sandbox_instance

        request = Mock()
        request.method = 'POST'
        request.POST = {'type': 'sandbox', 'compiler_report_id': self.compiler_report.pk}

        response = show(request, self.game.pk)
        mock_sandbox_instance.run.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, 'sandbox.html')

    def test_invalid_type_request(self):
        request = Mock()
        request.method = 'POST'
        request.POST = {'type': 'invalid_type'}

        response = show(request, self.game.pk)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, 'sandbox.html')

