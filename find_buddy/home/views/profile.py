from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

from find_buddy.home.models import Profile


class ProfileDitailView(DetailView):
    model = Profile
    template_name = 'profile-page.html'


class ProfileEditView(UpdateView):
    model = Profile
    fields = ['first_name', 'last_name', 'birth_date']
    template_name = 'profile-edit-page.html'

    def get_success_url(self):
        return reverse_lazy("show profile", kwargs={"pk": self.object.id})

