from django.contrib import admin
from .models import Post, Comment, Category


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'author', 'slug')
    list_display_links = ('title', 'author', 'slug')
    prepopulated_fields = {
        "slug": ("title",),
    }


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'name', 'email', 'publish', 'status')
    list_filter = ('status', 'publish')


admin.site.register(Post, AuthorAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category)
