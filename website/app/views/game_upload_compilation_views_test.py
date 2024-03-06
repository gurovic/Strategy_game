from django.test import TestCase, Client
from django.urls import reverse
from ..models import CompilerReport


class TestGameUploadCompilationView(TestCase):
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

        response = self.client.get(reverse('game_upload_compilation'))

        self.assertRedirects(response, reverse('game_upload_report'))

    def test_get_incomplete_reports(self):
        response = self.client.get(reverse('game_upload_compilation'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'game_upload.html')
        self.assertEqual(response.context['status'], 'compiling')
