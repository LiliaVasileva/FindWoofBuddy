from django.urls import path

from find_buddy.home.views.generic import UserLoginView, HomeTemplateView, UserRegistrationView, logout_then_login, \
    error_404, TestTemplateView
from find_buddy.home.views.password import UserPasswordResetView, UserPasswordResetDoneView, \
    UserPasswordResetConfirmView, UserPasswordResetCompleteView
from find_buddy.home.views.profile import ProfileDitailView, ProfileEditView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='profile login'),
    path('', HomeTemplateView.as_view(), name='home page'),
    path('register/', UserRegistrationView.as_view(), name='register user'),
    path('logout/', logout_then_login, name='profile logout'),
    path('error/', error_404, name='page 404'),
    path('profile/<int:pk>', ProfileDitailView.as_view(), name='show profile'),
    path('profile/edit/<int:pk>', ProfileEditView.as_view(), name='profile edit'),
    path('test/', TestTemplateView.as_view(), name='test'),
    path('password-reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done', UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/',UserPasswordResetCompleteView.as_view(),name='password_reset_complete')

    # done path('password-reset/', PasswordResetView.as_view(template_name='password/password-reset.html'), name='password_reset'),
    # done path('password-reset/done', PasswordResetDoneView.as_view(template_name='password/password-reset-done.html'), name='password_reset_done'),
    # done path('password-reset-confirm/<uidb64>/<token>', PasswordResetConfirmView.as_view(template_name='password/password-reset-confirm.html'), name='password_reset_confirm'),
    # path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name='password/password-reset-complete.html'), name='password_reset_complete'),
    #

]
