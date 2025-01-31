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


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'created_at')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'content', 'author', 'created_at')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Post,PostAdmin)
admin.site.register(Comment, CommentAdmin)