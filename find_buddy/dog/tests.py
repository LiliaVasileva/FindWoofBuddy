from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, Client
from django.urls import reverse
from django.test.client import RequestFactory

from find_buddy.dog.models import Dog, DogMissingReport
from find_buddy.dog.views import DogsTemplateView
from find_buddy.home.models import Profile

UserModel = get_user_model()


class DogsTemplateViewTest(TestCase):
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

    def test_if_it_render_correct_template(self):
        request = self.factory.get('dog/details//')
        request.user = self.user
        response = DogsTemplateView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual('dog/profile-dogs-page.html',response.template_name[0])

    def test_if_redirect_to_login_if_user_not_authenticated(self):
        request = self.factory.get('dog/details//')
        request.user = AnonymousUser()
        response = DogsTemplateView.as_view()(request)
        self.assertEqual(302,response.status_code)

    def test_if_return_correct_context_data(self):
        request = self.factory.get('dog/details//')
        request.user = self.user
        response = DogsTemplateView.as_view()(request)
        self.assertEqual(self.dog,response.context_data['dogs'][0])


class DogDetailsViewTest(TestCase):
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

    def test_if_it_render_correct_template(self):
        self.user.set_password('12345')
        self.user.save()
        self.client.login(email='testtestov@gmail.com', password='12345', )
        request = self.client.get(reverse('dog detail page', kwargs={'pk': self.dog.pk}))
        self.assertEqual(request.status_code, 200)
        self.assertEqual('dog/dog-details-page.html',request.template_name[0])

    def test_if_user_is_equal_to_request_user(self):
        self.user.set_password('12345')
        self.user.save()
        self.client.login(email='testtestov@gmail.com', password='12345', )
        request = self.client.get(reverse('dog detail page', kwargs={'pk': self.dog.pk}))
        self.assertEqual(self.user,request.wsgi_request.user)

    def test_if_returns_correct_context_data(self):
        self.user.set_password('12345')
        self.user.save()
        self.client.login(email='testtestov@gmail.com', password='12345', )
        request = self.client.get(reverse('dog detail page', kwargs={'pk': self.dog.pk}))
        self.assertTrue(True,request.context_data['is_owner'])


class DogEditViewTest(TestCase):
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

    def test_if_it_render_correct_template(self):
        self.user.set_password('12345')
        self.user.save()
        self.client.login(email='testtestov@gmail.com', password='12345', )
        request = self.client.get(reverse('dog edit', kwargs={'pk': self.dog.pk}))
        self.assertEqual(request.status_code, 200)
        self.assertEqual('dog/dog-edit-page.html',request.template_name[0])

    def test_when_editing_get_correct_update(self):
        self.user.set_password('12345')
        self.user.save()
        self.client.login(email='testtestov@gmail.com', password='12345', )
        request = self.client.post(reverse('dog edit', kwargs={'pk': self.dog.pk}),
                                   data={
                                       'name': 'Tom',
                                       'address': 'Varna, Sea Garden',
                                       'picture': 'IMG_20225454010_121818.jpg',
                                       'description': 'Some test here',
                                       'if_lost': False,
                                       'user': self.user,
                                   }
                                   )

        updated_dog = Dog.objects.get(pk=self.dog.pk)
        self.assertEqual('Tom',updated_dog.name)

    def test_when_edit_is_successful_redirect_correct(self):
        self.user.set_password('12345')
        self.user.save()
        self.client.login(email='testtestov@gmail.com', password='12345', )
        request = self.client.post(reverse('dog edit', kwargs={'pk': self.dog.pk}),
                                   data={
                                       'name': 'Tom',
                                       'address': 'Varna, Sea Garden',
                                       'picture': 'IMG_20225454010_121818.jpg',
                                       'description': 'Some test here',
                                       'if_lost': False,
                                       'user': self.user,
                                   }
                                   )

        updated_dog = Dog.objects.get(pk=self.dog.pk)
        self.assertEqual(302,request.status_code)


class DogMissingReportTest(TestCase):
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
        self.missing_report = DogMissingReport.objects.create(
            reported_address='Varna, Galata, Bulgaria',
            subject='Email subject',
            message='Lost dog',
            dog=self.dog,
        )
        self.client = Client()

    def test_when_invalid_address_is_filled_redirect_to_invalid(self):
        self.user.set_password('12345')
        self.user.save()
        self.client.login(email='testtestov@gmail.com', password='12345', )
        request = self.client.post(reverse('dog missing report'),
                                   data={
                                       'reported_address': 'fdlksjflksdf',
                                       'subject': 'Varna, Sea Garden',
                                       'message': 'IMG_20225454010_121818.jpg',
                                       'dog': self.dog.pk,
                                   }
                                   )

        self.assertEqual(302,request.status_code)

    def test_if_render_and_return_correct_status_code(self):
        self.user.set_password('12345')
        self.user.save()
        self.client.login(email='testtestov@gmail.com', password='12345', )
        request = self.client.get(reverse('dog missing report'))
        self.assertEqual(200,request.status_code)
