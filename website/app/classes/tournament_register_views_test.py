from django.contrib.auth.models import User
from django.test import TestCase

from app.models import Tournament


class TestRegisterInTournament(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.tournament = Tournament.objects.create(id=0)
        cls.user = User.objects.create_user(id=3, username='testuser', password='12345')

    def test_views_use_correct_template(self):
        response = self.client.get('/app/tournament/register/0/3')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register_intournament.html')

    def test_views_url_exists(self):
        response = self.client.get('/app/tournament/register/0/3')
        self.assertEqual(response.status_code, 200)

    def test_views_use_correct_context(self):
        response = self.client.get('/app/tournament/register/0/3')
        self.assertEqual(response.status_code, 200)
