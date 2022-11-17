from apps.users.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.db.models import Avg
from django.db.models.functions import Round


class RatingChoices(models.IntegerChoices):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


class RatingQuerySet(models.QuerySet):
    def rating(self):
        return self.aggregate(average=Round(Avg('value'), 1))['average']


class RatingManager(models.Manager):
    def get_queryset(self):
        return RatingQuerySet(model=self.model, using=self._db)


class Rating(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="rating")
    value = models.IntegerField(choices=RatingChoices.choices)
    content_type_user = models.ForeignKey(ContentType,
                                          on_delete=models.CASCADE,
                                          related_name='user')
    object_id_user = models.PositiveIntegerField()
    content_object_user = GenericForeignKey('content_type_user',
                                            'object_id_user')

    content_type_job = models.ForeignKey(ContentType,
                                         on_delete=models.CASCADE,
                                         related_name='job')
    object_id_job = models.UUIDField()
    content_object_job = GenericForeignKey('content_type_job', 'object_id_job')

    objects = RatingManager()
