from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from helpers.helpers import WORKING_CATEGORY
from accounting import managers


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=15, unique=True, null=False)
    phone_number_validation = models.BooleanField(default=False)
    national_code = models.IntegerField(null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    full_name = models.CharField(max_length=32, null=True, blank=True)
    join_date = models.DateTimeField(null=True, blank=True)
    birth_date = models.DateTimeField(null=True, blank=True)
    profile = models.ImageField(null=True, blank=True, upload_to='profiles/%Y/%m/')
    working_category = models.CharField(null=True, blank=True, choices=WORKING_CATEGORY, max_length=128, default='other')

    objects = managers.UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.phone_number} - {self.id}'

    @property
    def is_staff(self):
        return self.is_superuser


class OtpCode(models.Model):
    phone_number = models.CharField(max_length=20)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.phone_number} - {self.code} - {self.created}'
