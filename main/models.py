from django.db import models
from django.db.models.query_utils import select_related_descend


from django.contrib.auth import get_user_model
User = get_user_model()


# Create your models here.


class Region(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    location = models.ForeignKey(
        Region, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    seats = models.IntegerField(default=0, null=True)
    description = models.TextField(blank=True, verbose_name='Description')
    booked = models.BooleanField(default=False)
    event_date = models.TextField(max_length=100)
    age_limit = models.IntegerField(null=True)
    guests = models.ManyToManyField(User, through='Guest')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['booked']


class Discount(models.Model):
    discount = models.IntegerField(default=0)
    discount_age = models.IntegerField(default=0)
    event = models.OneToOneField(
        Event, on_delete=models.CASCADE, null=True, blank=True)


class Guest(models.Model):
    group = models.ForeignKey(
        Event, related_name="memberships", on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name='user_event', on_delete=models.CASCADE)
