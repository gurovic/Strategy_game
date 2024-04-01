from django.test import TestCase


class TestFrontedView(TestCase):
    def test_web_view_exists(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_web_view_use_correct_template(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'angular_index.html')
