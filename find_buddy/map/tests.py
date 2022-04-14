from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.test.client import RequestFactory

from find_buddy.home.models import Profile
from find_buddy.map.models import Search

UserModel = get_user_model()


class ShowMapViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
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
        self.search = Search.objects.create(
            address='Varna',
            date=date.today()

        )
        self.client = Client()

    def test_if_it_render_correct_template(self):
        self.user.set_password('12345')
        self.user.save()
        self.client.login(email='testtestov@gmail.com', password='12345', )
        request = self.client.get(reverse('map'))
        self.assertEqual(200,request.status_code)

    def test_if_redirect_to_404_if_address_is_not_valid(self):
        self.user.set_password('12345')
        self.user.save()
        self.client.login(email='testtestov@gmail.com', password='12345', )
        request = self.client.post(reverse('map'),
                                   data={
                                       'address': 'some invalid text here',
                                   }
                                   )

        self.assertEqual(302,request.status_code)

    def test_if_return_status_code_200_if_address_is_valid(self):
        self.user.set_password('12345')
        self.user.save()
        self.client.login(email='testtestov@gmail.com', password='12345', )
        request = self.client.post(reverse('map'),
                                   data={
                                       'address': 'Varna, Bulgaria',
                                   }
                                   )

        # when the address is valid it redirects to map view
        self.assertEqual(302, request.status_code)
