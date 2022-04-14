from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse

from find_buddy.dog.models import Dog
from find_buddy.home.models import Profile

UserModel = get_user_model()


class ProfileDitailViewTests(TestCase):
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

    def test_when_opening_not_existing_profile_expect_404(self):
        self.user.set_password('12345')
        self.user.save()
        self.client.login(email='testtestov@gmail.com', password='12345', )
        response = self.client.get(reverse('show profile', kwargs={'pk': 35}))
        self.assertEqual(404, response.status_code)

    def test_when_all_valid_expect_correct_template(self):
        self.user.set_password('12345')
        self.user.save()
        self.client.login(email='testtestov@gmail.com', password='12345', )
        request = self.client.get(reverse('show profile', kwargs={
            'pk': self.profile.pk
        }))
        self.assertEqual(request.template_name[0], 'profile-details-page.html')

    def test_when_user_is_owner__expect_is_owner_tobe_true(self):
        self.user.set_password('12345')
        self.user.save()
        self.client.login(email='testtestov@gmail.com', password='12345', )
        response = self.client.get(reverse('show profile', kwargs={'pk': self.profile.pk}))
        self.assertTrue(True, response.context['is_owner'])

    def test_when_user_is_not_owner__expect_is_owner_tobe_False(self):
        self.user.set_password('12345')
        self.user.save()
        self.client.login(email='testtestov@gmail.com', password='12345', )
        user2 = UserModel.objects.create(
            email='testtestov2@gmail.com',
            password='tetstetste2',
        )
        profile2 = Profile.objects.create(
            first_name='Test2',
            last_name='Testov2',
            picture='IMG_202202210_121818.jpg',
            birth_date=date(1991, 5, 6),
            user= user2,
        )

        response = self.client.get(reverse('show profile', kwargs={'pk': profile2.pk}))
        self.assertFalse(response.context['is_owner'])

    def test_when_user_has_dogs_shows_correct_dog(self):
        self.user.set_password('12345')
        self.user.save()
        self.client.login(email='testtestov@gmail.com', password='12345', )
        response = self.client.get(reverse('show profile', kwargs={'pk': self.profile.pk}))

        self.assertEqual(str(self.dog),''.join(response.context['dogs']))

    def test_when_user_has_no_dogs_dogs_should_be_empty(self):
        self.user.set_password('12345')
        self.user.save()
        self.client.login(email='testtestov@gmail.com', password='12345', )
        self.dog.delete()
        response = self.client.get(reverse('show profile', kwargs={'pk': self.profile.pk}))
        self.assertEqual('',response.context['dogs'])


