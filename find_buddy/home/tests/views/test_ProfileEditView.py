from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from find_buddy.home.models import Profile

UserModel = get_user_model()


class ProfileEditViewTests(TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'testtestov@gmail.com',
        'password': 'tetstetste',
    }
    VALID_PROFILE_DATA = {
        'first_name': 'Test',
        'last_name': '1123QwER',
        'picture': 'IMG_2022010_121818.jpg',
        'birth_date': date(1991, 3, 5),
    }

    def __create_user(self, **credentials):
        return UserModel.objects.create(**credentials)

    def __create_valid_user_and_profile(self):
        user = UserModel.objects.create(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(**self.VALID_PROFILE_DATA, user=user)
        return user, profile

    def test_when_editing_not_existing_profile_expect_404(self):
        response = self.client.get(reverse('profile edit', kwargs={'pk': 6}))
        self.assertEqual(404, response.status_code)

    def test_when_all_valid_expect_correct_template(self):
        user, profile = self.__create_valid_user_and_profile()

        response = self.client.get(reverse('profile edit', kwargs={
            'pk': profile.pk
        }))
        self.assertTemplateUsed(response, 'profile-edit-page.html')

    def test_when_editing_get_correct_update(self):
        user = UserModel.objects.create(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(**self.VALID_PROFILE_DATA, user=user)

        response = self.client.post(
            reverse('profile edit', kwargs={
                'pk': profile.pk,
            }),
            data={
                'first_name': 'Test5',
                'last_name': '1123QwER',
                'picture': 'IMG_2022010_121818.jpg',
                'birth_date': date(1991, 3, 5),
                'user': user,
            }
        )

        updated_profile = Profile.objects.get(pk=profile.pk)
        self.assertEqual('Test5', updated_profile.first_name)
