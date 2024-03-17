from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UA
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Profile

class UserAdmin(UA):
    list_display = ('username', 'email', "first_name", "last_name", 'is_staff', 'is_administrator')
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(User, UserAdmin)
admin.site.register(Profile)
