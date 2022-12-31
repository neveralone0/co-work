from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from helpers import helpers
from accounting import managers


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=15, unique=True, null=False)
    phone_number_validation = models.BooleanField(default=False)
    national_code = models.IntegerField(unique=True)
    user_code = models.IntegerField(null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    full_name = models.CharField(max_length=32, null=True, blank=True)
    birth_date = models.DateTimeField(null=True, blank=True)
    picture = models.ImageField(null=True, blank=True)

    objects = managers.UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.phone_number} - {self.id}'

    @property
    def is_staff(self):
        return self.is_superuser

    @property
    def is_admin(self):
        return self.role == helpers.ADMIN


# class InternProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#
#     first_name = models.CharField(null=True, blank=True, max_length=132)
#     last_name = models.CharField(null=True, blank=True, max_length=132)
#     personality_type = models.CharField(null=True, blank=True, max_length=4)
#     intern_code = models.CharField(null=True, blank=True, max_length=7)
#     picture = models.ImageField(null=True, blank=True)
#     emergency_phone = models.CharField(max_length=15, null=True, blank=True)
#     home_number = models.CharField(max_length=15, null=True, blank=True)  # make it unique later
#     gender = models.BooleanField(null=True, blank=True)
#     address = models.TextField(null=True, blank=True)
#     birth_date = models.DateTimeField(null=True, blank=True)
#     city = models.CharField(max_length=40)  # محل صدور شناسنامه
#     military_service = models.CharField(choices=helpers.MILITARY_STATUS_CHOICES, max_length=80)  # وضعیت خدمت
#     national_code = models.PositiveIntegerField(null=True, blank=True)  # add validation year / make it unique later
#     email = models.EmailField(null=True, blank=True)
#     marital = models.BooleanField(default=False, null=True, blank=True)
#
#     def __str__(self):
#         return f'{self.first_name}-{self.last_name}-{self.user.get_role_display()}'
#
#
# class InternProxy(User):
#     base_role = helpers.INTERN
#     objects = managers.InternManager()
#
#     class Meta:
#         proxy = True
#
#     # model methods here!
#     # get work_logs and so on ...


# class EducationInfo(models.Model):
#     pass


class Ban(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.DO_NOTHING, related_name='bans')
    end = models.DateTimeField()
    status = models.BooleanField(default=True)
    reason = models.CharField(max_length=255)


class OtpCode(models.Model):
    phone_number = models.CharField(max_length=20)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.phone_number} - {self.code} - {self.created}'
