from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.defaults import page_not_found
from django.views.generic import CreateView, TemplateView, ListView

from find_buddy.common.helpers import def_my_map
from find_buddy.dog.models import Dog
from find_buddy.home.forms import UserRegistrationForm
from find_buddy.home.models import Profile


class HomeTemplateView(TemplateView):
    template_name = 'home-page-no-profile.html'

    def get_context_data(self, *args, **kwargs):
        m = def_my_map()
        m = m._repr_html_()
        context = super().get_context_data(**kwargs)
        context['map'] = m
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)


class UserLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('dashboard')


class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'register.html'

    # to login when register
    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)
        return result

    def get_success_url(self):
        return reverse_lazy('dashboard')


def logout_then_login(request):
    login_url = 'profile login'
    return LogoutView.as_view(next_page=login_url)(request)


def error_404(request):
    return render(request, 'page-404.html')


class ProfileHomeListView(ListView):
    model = Dog
    template_name = 'home-page-with-profile.html'
    paginate_by = 2
    context_object_name = 'dogs'
    ordering = ['-if_lost']


