from django.contrib import admin

# Register your models here.
from .models import Post,Comment, PostImage

class PostAdmin(admin.ModelAdmin):
    list_display = ('user','created_at')

admin.site.register(Post,PostAdmin)
admin.site.register(Comment)
admin.site.register(PostImage)