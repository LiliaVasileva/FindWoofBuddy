from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from find_buddy.dog.models import Dog
from find_buddy.home.models import Profile

UserModel = get_user_model()


class ProfileDitailViewTests(TestCase):
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
    VALID_DOG_DATA = {
        'name': 'Tom',
        'address': 'Sofia, Lake Park',
        'picture': 'IMG_20220090_121818.jpg',
        'description': 'Some Text Here',
        'if_lost': 'False',
    }
    VALID_DOG_DATA_2 = {
        'name': 'Jerry',
        'address': 'Varna, Bulgaria',
        'picture': 'IMG_20220454090_121818.jpg',
        'description': 'Some Text Here',
        'if_lost': 'False',
    }

    def __create_user(self, **credentials):
        return UserModel.objects.create(**credentials)

    def __create_valid_user_and_profile(self):
        user = UserModel.objects.create(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(**self.VALID_PROFILE_DATA, user=user)
        return user, profile

    def test_when_opening_not_existing_profile_expect_404(self):
        response = self.client.get(reverse('show profile', kwargs={'pk': 35}))
        self.assertEqual(404, response.status_code)

    def test_when_all_valid_expect_correct_template(self):
        user = UserModel.objects.create(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(**self.VALID_PROFILE_DATA, user=user)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('show profile', kwargs={
            'pk': profile.pk
        }))
        a=5
        self.assertTemplateUsed(response.path, 'profile-details-page.html')

    def test_when_user_is_owner__expect_is_owner_tobe_true(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('show profile', kwargs={'pk': profile.pk}))

        self.assertTrue(True, response.context['is_owner'])

    def test_when_user_is_not_owner__expect_is_owner_tobe_False(self):
        user, profile = self.__create_valid_user_and_profile()
        credentials = {
            'email': 'test1@gmail.com',
            'password': '1123QwER',
        }
        user2 = self.__create_user(**credentials)

        self.client.login(**credentials)
        response = self.client.get(reverse('show profile', kwargs={'pk': profile.pk}))

        self.assertFalse(response.context['is_owner'])

    def test_when_user_has_dogs_shows_correct_dog(self):
        user, profile = self.__create_valid_user_and_profile()
        dog = Dog.objects.create(**self.VALID_DOG_DATA, user=user)
        user_2 = UserModel.objects.create(**{'email': 'testov3@abv.bg', 'password': '1123QbBQw$E'})
        dog_user_2 = Dog.objects.create(**self.VALID_DOG_DATA_2, user=user_2)
        response = self.client.get(reverse('show profile', kwargs={'pk': profile.pk}))

        self.assertEqual(str(dog), ''.join(response.context['dogs']))

    def test_when_user_has_no_dogs_dogs_should_be_empty(self):
        user, profile = self.__create_valid_user_and_profile()
        response = self.client.get(reverse('show profile', kwargs={'pk': profile.pk}))
        self.assertEqual('',response.context['dogs'])


