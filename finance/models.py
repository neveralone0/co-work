from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from accounting.models import User


class Bill(models.Model):
    price = models.PositiveIntegerField()
    user = models.OneToOneField(to=User, on_delete=models.DO_NOTHING)
    date = models.DateTimeField(auto_now=True)
    is_payed = models.BooleanField(default=False)
    discount = models.IntegerField(blank=True, null=True, default=None)


class Coupon(models.Model):
    code = models.CharField(max_length=30, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(90)])
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.code
