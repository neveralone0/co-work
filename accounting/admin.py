# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .forms import UserCreationForm, UserChangeForm
# from .models import User
#
#
# class UserAdmin(BaseUserAdmin):
#     form = UserChangeForm
#     add_form = UserCreationForm
#
#     list_display = ('email', 'phone_number', 'is_superuser')
#     list_filter = ('is_superuser',)
#
#     # shows in admin panel
#     fieldsets = (
#         ('Personal information', {'fields': ('email', 'phone_number', 'fullname', 'password')}),
#         ('Permissions', {'fields': ('is_active', 'is_superuser', 'last_login')}),
#     )
#
#     # superuser register
#     add_fieldsets = (
#         (None, {'fields': ('phone_number', 'email', 'fullname', 'password1', 'password2')}),
#     )
#
#     search_fields = ('email',)
#     ordering = ('fullname',)
#     filter_horizontal = ()
#
#
# admin.site.register(User, UserAdmin)

from django.contrib import admin
from accounting.models import User, Ban, OtpCode


admin.site.register(User)
admin.site.register(Ban)
admin.site.register(OtpCode)

