from django.contrib import admin

from jwt_authenticate.models import UserLogin


@admin.register(UserLogin)
class UserLoginAdmin(admin.ModelAdmin):
    pass
