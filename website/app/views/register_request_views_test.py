from django.test import TestCase
from ..forms import NewUserForm
class TestRegisterRequestViews(TestCase):
    def test_views_use_correct_template(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)
        #self.assertTemplateUsed(response, 'register.html')

    def test_views_url_exists(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_views_use_correct_context(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_registration(self):
        form = NewUserForm(data={'username': 'example_username_1234',
                                 'email': 'mail@example.com',
                                 'password1': 'qwerty1234test_password',
                                 'password2': 'qwerty1234test_password'})
        self.failUnless(form.is_valid())