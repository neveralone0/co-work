from django.db import models
from core.settings import BASE_DIR


class Images(models.Model):
    img = models.ImageField(upload_to=BASE_DIR / 'static/%Y/%m/')


class Cards(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    # lis = models.ForeignKey(to='Li',on_delete=models.SET_DEFAULT, default='')
    li1 = models.CharField(max_length=128)
    li2 = models.CharField(max_length=128)
    li3 = models.CharField(max_length=128)

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
