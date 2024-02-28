from django.test import TestCase, Client
from django.urls import reverse
from ..models import CompilerReport, Game


class TestGameUploadReportView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get(self):
        ideal_solution_report = CompilerReport.objects.create()
        play_report = CompilerReport.objects.create()
        visualiser_report = CompilerReport.objects.create()

        session = self.client.session
        session['ideal_solution_report_id'] = ideal_solution_report.id
        session['play_report_id'] = play_report.id
        session['visualiser_report_id'] = visualiser_report.id
        session.save()

        response = self.client.get(reverse('game_upload_report'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'game_upload.html')
        self.assertEqual(response.context['status'], 'receive compiler report')

    def test_post_game_upload(self):
        game = Game.objects.create(id=1, name='Test Game')

        session = self.client.session
        session['game_id'] = game.id
        session.save()

        response = self.client.post(reverse('game_upload_report'), {'type': 'game'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'game_upload.html')
        self.assertEqual(response.context['status'], 'game uploaded')
        self.assertEqual(response.context['game_name'], 'Test Game')
        self.assertTrue(self.client.session['game_been_uploaded'])

    def test_post_dont_upload(self):
        game = Game.objects.create(id=1, name='Test Game')

        session = self.client.session
        session['game_id'] = game.id
        session.save()

        response = self.client.post(reverse('game_upload_report'), {'type': 'dont upload'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('game_upload_form'))

        self.assertFalse(Game.objects.filter(id=game.id).exists())

    def test_post_new_game(self):
        response = self.client.post(reverse('game_upload_report'), {'type': 'new game'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('game_upload_form'))