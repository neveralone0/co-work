from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password, national_code, is_super_user=False, **kwargs):
        user = self.model(
            phone_number=phone_number,
            national_code=national_code,
            last_login=timezone.now(),
        )
        if is_super_user:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password, **kwargs):
        user = self.create_user(phone_number, password, national_code=None, is_super_user=True, **kwargs)
        user.is_superuser = True
        user.save(using=self._db)
        return user
