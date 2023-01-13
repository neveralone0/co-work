from django.db import models
from core.settings import BASE_DIR
from accounting.models import User


def upload_to(instance, filename):
    return '/site{filename}'.format(filename=filename)


class Images(models.Model):
    img = models.ImageField(upload_to=upload_to)


class Cards(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    # lis = models.ForeignKey(to='Li',on_delete=models.SET_DEFAULT, default='')
    li1 = models.CharField(max_length=128, null=True, blank=True)
    li2 = models.CharField(max_length=128, null=True, blank=True)
    li3 = models.CharField(max_length=128, null=True, blank=True)

#
# class Li(models.Model):
#     text = models.CharField(max_length=128)
#     card = models.ForeignKey(to=Cards, on_delete=models.CASCADE, related_name='lis', null=True, blank=True)


class ContactUs(models.Model):
    address = models.CharField(max_length=512)
    work_time = models.CharField(max_length=256)
    access_ways = models.CharField(max_length=128)
    langtitude = models.CharField(max_length=256)
    longtitude = models.CharField(max_length=256)
    instagram = models.CharField(max_length=32)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()


class Ban(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, related_name='bans')
    end = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    reason = models.CharField(max_length=255)


class Quotes(models.Model):
    title = models.CharField(max_length=64, null=True, blank=True)
    body = models.CharField(max_length=256, null=True, blank=True)


class Income(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    desk_count = models.IntegerField(null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)