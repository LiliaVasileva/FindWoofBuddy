from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from find_buddy.home.models import Profile

UserModel = get_user_model()


class RequestFactory:
    pass


request = RequestFactory().get('/')
view = HomeView()
view.setup(request)

context = view.get_context_data()
self.assertIn('environment', context)


class ShowMapViewTest(TestCase):
    def test_when_there_is_not_only_letters_expect_to_raise_ValidationError(self):
        request = RequestFactory()
        request.get('map')
        response = self.client.get(reverse('map'))
        self.assertTemplateUsed(response, 'home-map.html')


    # def test_when_there_is_only_letters_expect_to_do_nothing(self):
    #     value = 'Test'
    #     self.assertEqual(None, validate_only_letters(value))


