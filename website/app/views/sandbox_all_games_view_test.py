from django.test import TestCase
from ..models import Game, Tournament

class TestSandboxAllGames(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.game1 = Game.objects.create(id=1)
        cls.game2 = Game.objects.create(id=2)
        cls.game3 = Game.objects.create(id=3)
        cls.all_games = [cls.game1, cls.game2, cls.game3]

    def test_views_url_exists(self):
        response = self.client.get('/app/sandbox/')
        self.assertEqual(response.status_code, 200)

    def test_views_use_correct_template(self):
        response = self.client.get('/app/sandbox/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sandbox_all_games.html')

    def test_games_added(self):
        response = self.client.get('/app/sandbox/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['available_games']),
                                 self.all_games)
