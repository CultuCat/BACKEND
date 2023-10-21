from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Comment Information', {'fields': ['user', 'event', 'text']}),
    ]
    list_display = ('id', 'user', 'event', 'text', 'created_at')
