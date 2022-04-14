from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse

from find_buddy.common.helpers import def_my_map
from find_buddy.home.models import Profile

UserModel = get_user_model()


class HomeTemplateViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.test_map = def_my_map()
        self.user = UserModel.objects.create(
            email='testtestov@gmail.com',
            password='tetstetste',
        )
        self.profile = Profile.objects.create(
            first_name='Test',
            last_name='Testov',
            picture='IMG_2022010_121818.jpg',
            birth_date=date(1991, 4, 6),
            user=self.user,
        )

    def test_if_user_is_authenticated_redirect_to_dashboard(self):
        self.user.set_password('12345')
        self.user.save()
        self.client.login(email='testtestov@gmail.com', password='12345', )
        response = self.client.get(reverse('home page'))
        self.assertEqual(302, response.status_code)

    def test_if_render_correct_context_data(self):
        response = self.client.get(reverse('home page'))
        test_map =  self.test_map._repr_html_()
        self.assertTrue(test_map, response.context['map'])