from django.contrib import admin
from blog.models import Post, Tag
# Register your models here.

@admin.register(Post)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'contents', 'created_at', 'updated_at']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']