from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from find_buddy.common.validators import validate_only_letters
from find_buddy.home.managers import FindBuddyUserManager


class FindBuddyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )
    is_staff = models.BooleanField(
        default=False,
    )
    USERNAME_FIELD = 'email'

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )
    is_active = models.BooleanField(default=True)

    objects = FindBuddyUserManager()


class Profile(models.Model):
    first_name = models.CharField(
        max_length=25,
        validators=(
            validate_only_letters,
        )
    )
    last_name = models.CharField(
        max_length=30,
        validators=(
            validate_only_letters,
        )
    )

    picture = models.ImageField(
        blank=True,
        null=True,
    )

    birth_date = models.DateField()

    user = models.OneToOneField(
        FindBuddyUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.full_name}'

    class Meta:
        verbose_name = 'Profile'
