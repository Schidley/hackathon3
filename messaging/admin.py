# admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Post
from .models import Comment

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('bio', 'profile_picture')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Post)
admin.site.register(Comment)