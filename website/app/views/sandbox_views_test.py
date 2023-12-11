import time

from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import Mock, patch

from app.models import CompilerReport

class TestSandboxViews(TestCase):
    def setUpTestData():
        CompilerReport.objects.create(
            compiled_file=None,
            status=0,
        )

    def test_views_url_exists(self):
        response = self.client.get('/app/sandbox/0')
        self.assertEqual(response.status_code, 200)

    def test_views_use_correct_template(self):
        response = self.client.get('/app/sandbox/0')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sandbox_views.html')

    def test_views_use_correct_context(self):
        response = self.client.get('/app/sandbox/0')
        self.assertEqual(response.status_code, 200)
