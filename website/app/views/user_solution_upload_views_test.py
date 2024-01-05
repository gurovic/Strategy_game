from django.test import TestCase


class testUserSolutionUploadViews(TestCase):
    def test_user_solution_upload_uses_correct_template(self):
        response = self.client.get('/app/tournament/upload')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sandbox_views.html')