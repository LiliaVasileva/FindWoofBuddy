from django.contrib.auth import get_user_model
from django.db import models

from find_buddy.common.validators import validate_only_letters

UserModel = get_user_model()


class Dog(models.Model):
    DOG_NAME_MAX_LEN = 80
    DOG_ADDRESS_MAX_LEN = 255

    name = models.CharField(
        max_length=DOG_NAME_MAX_LEN,
        validators=(
            validate_only_letters,
        )
    )
    address = models.CharField(
        max_length=DOG_ADDRESS_MAX_LEN,
    )
    picture = models.ImageField(
        null=True,
        blank=True,
    )

    description = models.TextField(
        null=True,
        blank=True,
    )
    if_lost = models.BooleanField(
        default=False,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ('user', 'name')
