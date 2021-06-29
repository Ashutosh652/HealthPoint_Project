from django.contrib import admin
from .models import Post, Comment


admin.site.register(Post)
admin.site.register(Comment)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'post', 'date_commented')
    list_filter = ('date_commented')
    search_fields = ('author', 'content')
