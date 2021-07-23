
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from main.models import Region


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    age = models.IntegerField(default=0)
    region = models.ForeignKey(Region, on_delete=CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__():
        return Profile.user
