from django.contrib import admin
from .models import CustomUser


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_admin')


admin.site.register(CustomUser, UserAdmin)