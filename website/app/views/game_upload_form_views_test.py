from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import SimpleUploadedFile

from unittest.mock import Mock, patch
from ..models import Game


class TestGameUploadFormView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get(reverse('game_upload_form'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'game_upload.html')

    def test_post(self):
        request = Mock()
        request.method = 'POST'

        response = self.client.post(reverse('game_upload_form'), {
            'name': 'Test Game',
            'number_of_players': 4,
            'win_point': 10,
            'lose_point': 5,
            'ideal_solution': SimpleUploadedFile("test_ideal_solution.py", b"file_content"),
            'play': SimpleUploadedFile("test_play.py", b"file_content"),
            'visualiser': SimpleUploadedFile("test_visualiser.py", b"file_content"),
            'rules': SimpleUploadedFile("test_rules.txt", b"file_content"),
            'ideal_solution_language': 'py',
            'play_language': 'py',
            'visualiser_language': 'py',
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Game.objects.count(), 1)
        self.assertNotEqual(request.session.get('game_id'), 0)