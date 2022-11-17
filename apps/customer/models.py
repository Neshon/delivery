from django.db import models

from apps.users.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # avatar = models.ImageField(upload_to='customer/avatar/',
    #                            blank=True,
    #                            null=True)
    # phone_number = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.user.get_full_name()
