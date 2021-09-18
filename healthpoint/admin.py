from django.contrib import admin
from .models import Post, Comment, Notification

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'date_commented')
    search_fields = ('author__user_name', 'content')

class PostAdmin(admin.ModelAdmin):
    list_display = ('title' ,'author', 'date_posted')
    search_fields = ('author', 'content')



admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Notification)