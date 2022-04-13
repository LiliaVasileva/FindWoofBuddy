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

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('user', 'name')


class DogMissingReport(models.Model):
    REPORTED_ADDRESS_MAX_LEN = 255
    SUBJECT_MAX_LEN = 255
    reported_address = models.CharField(
        max_length=REPORTED_ADDRESS_MAX_LEN,
        verbose_name='Report an address'
    )
    subject = models.CharField(
        max_length=SUBJECT_MAX_LEN,
        null=True,
        blank=True,
        verbose_name='Subject'
    )
    message = models.TextField(
        null=True,
        blank=True,
        verbose_name='Message'

    )
    dog = models.ForeignKey(
        Dog,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.subject

