from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from find_buddy.dog.models import Dog
from find_buddy.home.models import Profile

UserModel = get_user_model()


class ProfileEditViewTests(TestCase):
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
        self.dog = Dog.objects.create(
            name='Billy',
            address='Varna, Sea Garden',
            picture='IMG_2022d86583010_121818.jpg',
            description='Some Text Here',
            if_lost=False,
            user=self.user
        )
        self.client = Client()

    def test_when_open_not_existing_profile_expect_302_to_login_page(self):
        response = self.client.get(reverse('profile edit', kwargs={'pk': 6}))
        self.assertEqual(302, response.status_code)

    def test_when_all_valid_expect_correct_template(self):
        self.user.set_password('12345')
        self.user.save()
        self.client.login(email='testtestov@gmail.com', password='12345', )
        response = self.client.get(reverse('profile edit', kwargs={
            'pk': self.profile.pk
        }))
        self.assertTemplateUsed(response, 'profile-edit-page.html')

    def test_when_editing_get_correct_update(self):
        self.user.set_password('12345')
        self.user.save()
        self.client.login(email='testtestov@gmail.com', password='12345', )
        request=self.client.post(
            reverse('profile edit', kwargs={'pk': self.profile.pk, }),data=
            {
                'first_name': 'Testv',
                'last_name': 'TestTest',
                'picture': 'IMG_2022010_121818.jpg',
                'birth_date': date(1991, 3, 5),
                'user': self.user,
            }
        )
        updated_profile = Profile.objects.get(pk=self.profile.pk)
        self.assertEqual('Testv', updated_profile.first_name)
