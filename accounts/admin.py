from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import User, UserFollow
from accounts.forms import UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'email', 'is_active', 'is_admin', 'user_followers', 'user_followings')
    list_filter = ('is_active', 'is_admin')
    readonly_fields = ('last_login',)

    fieldsets = (
        (None, {
            "fields": ('username', 'email', 'password', 'first_name', 'last_name'),
        }),
        ('permissions', {
            "fields": ('is_active', 'is_admin', 'is_superuser', 'last_login', 'groups', 'user_permissions')
        }),
    )

    add_fieldsets = (
        (None, {
            "fields": ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        }),
    )

    search_fields = ('username', 'email')
    ordering = ('-id',)
    filter_horizontal = ('groups', 'user_permissions')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            superuser_field = form.base_fields.get('is_superuser')
            if superuser_field:
                superuser_field.disabled = True
            admin_field = form.base_fields.get('is_admin')
            if admin_field:
                admin_field.disabled = True
        return form

    def user_followers(self, obj):
        return obj.followers.count()

    def user_followings(self, obj):
        return obj.followings.count()

    user_followers.short_description = 'followers'
    user_followings.short_description = 'following'


admin.site.register(User, UserAdmin)


@admin.register(UserFollow)
class UserFollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following')
