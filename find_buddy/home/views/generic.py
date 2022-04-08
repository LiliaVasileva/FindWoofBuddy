from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.defaults import page_not_found
from django.views.generic import CreateView, TemplateView

from find_buddy.common.helpers import def_my_map
from find_buddy.home.forms import UserRegistrationForm


class HomeTemplateView(TemplateView):
    template_name = 'home-page-no-profile.html'

    def get_context_data(self, *args, **kwargs):
        m = def_my_map()
        context = super().get_context_data(**kwargs)
        context['map'] = m
        return context


class UserLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('test')


class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'register.html'

    def get_success_url(self):
        return reverse_lazy("show profile", kwargs={"pk": self.object.id})

    # to login when register
    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)
        return result


def logout_then_login(request):
    login_url = 'profile login'
    return LogoutView.as_view(next_page=login_url)(request)


def error_404(request):
    return render(request, 'page-404.html')


class TestTemplateView(TemplateView):
    template_name = 'home-page-with-profile.html'
