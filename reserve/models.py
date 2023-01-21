from django.db import models
from accounting.models import User


class Desk(models.Model):
    active = models.BooleanField(default=True)
    price = models.PositiveIntegerField()
    id = models.IntegerField(unique=True, primary_key=True)

    def __str__(self):
        return f'{self.id}'


class Reservation(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, null=True, blank=True)
    desk = models.ForeignKey(to=Desk, on_delete=models.DO_NOTHING)
    is_group = models.BooleanField(default=False, null=True, blank=True)
    payment = models.BooleanField(default=False)
    reservation_time = models.DateField()
    order_time = models.DateField(auto_now=True, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.desk.id} - {self.payment}'
