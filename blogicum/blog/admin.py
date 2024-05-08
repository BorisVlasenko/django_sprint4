from django.contrib import admin
from .models import Post, Category, Location, Comment


admin.site.register(Post)
admin.site.register(Location)
admin.site.register(Category)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'author', 'text']
