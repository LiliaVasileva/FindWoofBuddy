from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView


class UserPasswordResetView(PasswordResetView):
    template_name = 'password/password-reset.html'


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password/password-reset-done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password/password-reset-confirm.html'


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password/password-reset-complete.html'
