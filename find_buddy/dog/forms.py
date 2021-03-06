from django import forms
from django.contrib import messages
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.http import request

from find_buddy.common.form_mixins import BootstrapFormMixin, DisabledFieldsFormMixin
from find_buddy.dog.models import Dog, DogMissingReport


class DogCreateForm(BootstrapFormMixin, forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        dog = super().save(commit=False)
        dog.user = self.user
        if commit:
            dog.save()
        return dog

    class Meta:
        model = Dog
        fields = ['name', 'address', 'picture', 'description']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter dog name',
                }
            ),
            'address': forms.TextInput(
                attrs={
                    'placeholder': 'Most popular walking spot'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'placeholder': "Woof's information",
                    'rows': 3,
                }
            ),
        }
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "You already own Woof with that name.",
            }
        }


class DogEditForm(forms.ModelForm, BootstrapFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = Dog
        exclude = ['user', 'if_lost']

        widgets = {
            'description': forms.Textarea(
                attrs={
                    'rows': 3,
                }
            ),
        }


class DogDeleteForm(forms.ModelForm, DisabledFieldsFormMixin, BootstrapFormMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()
        self._init_disabled_fields()

    def save(self, commit=True):
        if commit:
            self.instance.delete()
        return self.instance

    class Meta:
        model = Dog
        exclude = ['user', 'if_lost', 'picture']
        widgets = {
            'description': forms.Textarea(
                attrs={
                    'rows': 3,
                }
            ),
        }


class DogMissingReportForm(forms.ModelForm, BootstrapFormMixin):
    def __init__(self, *args,user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()
        self.user =user
        a=5
        self.fields['dog'] = forms.ModelChoiceField(queryset=Dog.objects.filter(user=user))

    class Meta:
        model = DogMissingReport
        fields ='__all__'
        widgets = {
            'reported_address': forms.Textarea(
                attrs={
                    'rows': 1,
                    'placeholder': 'Woof last seen address',
                }
            ),
            'subject': forms.Textarea(
                attrs={
                    'rows': 1,
                    'placeholder': 'Email subject',
                }
            ),
            'message': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'Email message to the owners nearby',
                }
            ),
        }