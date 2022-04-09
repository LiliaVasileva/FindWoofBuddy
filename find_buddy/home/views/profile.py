from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

from find_buddy.dog.models import Dog
from find_buddy.home.models import Profile


class ProfileDitailView(DetailView):
    model = Profile
    template_name = 'profile-details-page.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dogs_list = Dog.objects.filter(user_id=self.object.user_id)
        dogs = [str(dog.name) for dog in dogs_list]

        context.update({
            'dogs': dogs,
            'is_owner': self.object.user_id == self.request.user.id,
        })

        return context


class ProfileEditView(UpdateView):
    model = Profile
    fields = ['picture','first_name', 'last_name', 'birth_date']
    template_name = 'profile-edit-page.html'

    def get_success_url(self):
        return reverse_lazy("show profile", kwargs={"pk": self.object.pk})

