from django.db import models
from accounting.models import User


class Desk(models.Model):
    active = models.BooleanField(default=True)
    price = models.PositiveIntegerField()
    id = models.IntegerField(unique=True, primary_key=True)


class Reservation(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.DO_NOTHING, null=True, blank=True)
    desk = models.OneToOneField(to=Desk, on_delete=models.DO_NOTHING)
    cancel_status = models.BooleanField(default=False)  # canceled or not
    reservation_time = models.DateTimeField()
