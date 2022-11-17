from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    avatar = models.ImageField(upload_to='customer/avatar/',
                               blank=True,
                               null=True)
    phone_number = PhoneNumberField(blank=True)

    def __str__(self):
        return self.get_full_name()
