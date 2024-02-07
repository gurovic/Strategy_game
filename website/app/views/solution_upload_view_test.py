from django.test import TestCase
from django.test import TestCase
import unittest
from ..forms import TournamentForm

from django.urls import reverse
from django.http import HttpRequest
from django.contrib.auth.models import User
from unittest.mock import Mock, patch

from app.models import CompilerReport, Tournament
from app.views import solution_upload_view

class testUserSolutionUploadViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tournament = Tournament.objects.create(id=0)
        cls.user = User.objects.create_user(id=0, username='testuser', password='12345')

    def test_views_use_correct_template(self):
        response = self.client.get('/app/tournament/upload_solution/0/0')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'solution_upload.html')

    def test_views_url_exists(self):
        response = self.client.get('/app/tournament/upload_solution/0/0')
        self.assertEqual(response.status_code, 200)

    def test_views_use_correct_context(self):
        response = self.client.get('/app/tournament/upload_solution/0/0')
        self.assertEqual(response.status_code, 200)

    def test_status_upload(self):
