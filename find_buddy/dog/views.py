from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView
from geopy import Nominatim
from geopy.distance import geodesic

from find_buddy.common.variables import SEARCHING_SURROUNDING_DISTANCE
from find_buddy.dog.forms import DogCreateForm, DogEditForm, DogDeleteForm, DogMissingReportForm
from find_buddy.dog.models import Dog
from find_buddy.settings import EMAIL_HOST_USER


class DogsTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'dog/profile-dogs-page.html'
    login_url = 'profile login'
    redirect_field_name = 'profile login'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        dogs = list(Dog.objects.filter(user=self.request.user))

        context.update({
            'dogs': dogs,
        })
        return context


class DogDetailsView(LoginRequiredMixin, DetailView):
    model = Dog
    template_name = 'dog/dog-details-page.html'
    context_object_name = 'dog'
    login_url = 'profile login'
    redirect_field_name = 'profile login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'is_owner': self.object.user_id == self.request.user.id,
        })
        return context


class DogCreateView(LoginRequiredMixin, CreateView):
    form_class = DogCreateForm
    template_name = 'dog/dog-create-page.html'
    login_url = 'profile login'
    redirect_field_name = 'profile login'

    def get_success_url(self):
        return reverse_lazy('owner dogs')

    # this way we define the pet to be created for the currant user
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class DogEditView(LoginRequiredMixin, UpdateView):
    model = Dog
    form_class = DogEditForm
    template_name = 'dog/dog-edit-page.html'
    login_url = 'profile login'
    redirect_field_name = 'profile login'

    def get_success_url(self):
        return reverse_lazy('owner dogs')


@login_required(login_url='profile login')
def dog_delete_view(request, pk):
    dog = Dog.objects.get(pk=pk)
    if request.method == 'POST':
        form = DogDeleteForm(request.POST, request.FILES, instance=dog)
        if form.is_valid():
            form.save()
            return redirect('owner dogs')
    else:
        form = DogDeleteForm(instance=dog)
    context = {
        'form': form,
        'dog': dog,
    }
    return render(request, 'dog/dog-delete-page.html', context)


@login_required(login_url='profile login')
def dog_missing_report(request):
    if request.method == 'POST':
        form = DogMissingReportForm(request.POST, user=request.user)
        missing_dog = form.dog
        missing_dog.if_lost = True
        missing_dog.save()
        if form.is_valid():
            geolocator = Nominatim(user_agent='dog')
            reported_address_ = form.cleaned_data['reported_address']
            reported_address = geolocator.geocode(reported_address_)
            reported_address_lat = reported_address.latitude
            reported_address_long = reported_address.longitude
            point_a = (reported_address_lat, reported_address_long)
            recipient_list = []

            for dog in Dog.objects.all():
                dog_address = geolocator.geocode(dog.address)
                dog_address_lat = dog_address.latitude
                dog_address_long = dog_address.longitude
                point_b = (dog_address_lat, dog_address_long)
                distance = round(geodesic(point_a, point_b).km, 2)
                if distance < SEARCHING_SURROUNDING_DISTANCE:
                    recipient_list.append(dog.user.email)
            if recipient_list:
                subject = form.cleaned_data['subject']
                message = form.cleaned_data['message']
                send_mail(subject, message, from_email=EMAIL_HOST_USER, recipient_list=recipient_list)
            form.save()
            return redirect('dashboard')
    else:
        form = DogMissingReportForm(user=request.user)

    context = {
        'form': form,
    }

    return render(request, 'dog/dog-missing-report.html', context)
