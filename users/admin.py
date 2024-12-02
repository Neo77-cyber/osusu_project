# users/admin.py

from django.contrib import admin
from .models import *

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'phone_number')
    search_fields = ('email', 'username', 'first_name', 'last_name', 'phone_number')


class UserGroupAdmin(admin.ModelAdmin):
    filter_horizontal = ('members',)  
    list_display = ('name', 'member_count')

    def member_count(self, obj):
        return obj.members.count()

admin.site.register(UserGroup, UserGroupAdmin)
