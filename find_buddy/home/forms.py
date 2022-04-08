from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from find_buddy.common.form_mixins import BootstrapFormMixin
from find_buddy.home.models import Profile

UserModel = get_user_model()


class UserRegistrationForm(UserCreationForm,BootstrapFormMixin):
    first_name = forms.CharField(
        max_length=30,
    )
    last_name = forms.CharField(
        max_length=30,
        error_messages=None,
    )
    birth_date = forms.DateField(
        widget=forms.TextInput(attrs={'placeholder': 'Year-Month-Date'}),
        error_messages=None,
    )

    class Meta:
        model = UserModel
        fields = ('email',)

    def clean_first_name(self):
        return self.cleaned_data['first_name']

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            birth_date=self.cleaned_data['birth_date'],
            user=user,
        )
        if commit:
            profile.save()
        return user


