# from django.contrib.auth.models import BaseUserManager
#
#
# class CustomUserManager(BaseUserManager):
#     def create_intern(self, phone_number, fullname, password, **kwargs):
#         user = self.model(phone_number=phone_number, fullname=fullname, password=password, role='i')
#         user.set_password(password)
#         user.save()
#         return user
#
#     def create_superuser(self, phone_number, password, **kwargs):
#         user = self.model(phone_number=phone_number, password=password)
#         user.set_password(password)
#         user.is_superuser = True
#         user.save()
#         return user

from django.contrib.auth.models import BaseUserManager
from django.utils import timezone

from accounting import models
from helpers import helpers


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password, is_super_user=False, **kwargs):
        user = self.model(
            phone_number=phone_number,
            national_code=1,
            last_login=timezone.now(),
        )
        if is_super_user:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user
    #
    # def create_intern(self, phone_number, password, **kwargs):
    #     user = self._create_user(phone_number, password, **kwargs)
    #     user.role = helpers.INTERN
    #     user.save(using=self._db)
    #     return user

    def create_superuser(self, phone_number, password, **kwargs):
        user = self.create_user(phone_number, password, is_super_user=True, **kwargs)
        user.is_superuser = True
        user.save(using=self._db)
        return user

#
# class InternManager(BaseUserManager):
#     def get_queryset(self, *args, **kwargs):
#         return super().get_queryset(*args, **kwargs).filter(role=helpers.INTERN)
    #
    # def create(self, user, **kwargs):
    #     if not user.role == helpers.INTERN:
    #         raise ValidationError('"User" object must have "intern" role.')
    #
    #     user = models.InternProfile.objects.create(user=user, **kwargs)
    #     user.save()
    #     return user
