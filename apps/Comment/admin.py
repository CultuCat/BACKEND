from django.contrib import admin
from .apps import Comment

class CommentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['user']}),
        (None,               {'fields': ['event']}),
        (None,               {'fields': ['text']}),
        (None,               {'fields': ['created_at']})
    ]
    list_display =  ('id', 'user', 'event', 'text', 'created_at')
admin.site.register(Comment, CommentAdmin)