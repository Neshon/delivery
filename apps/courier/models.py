from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Avg

from apps.ratings.models import Rating


class Courier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lat = models.FloatField(default=0)
    lng = models.FloatField(default=0)
    ratings = GenericRelation(Rating, related_query_name='courier')

    def __str__(self):
        return self.user.get_full_name()

    def get_rating(self):
        return Courier.objects.filter(id=self.id).aggregate(
            Avg('ratings__value'))
