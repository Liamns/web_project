from django.contrib import admin

# Register your models here.

from .models import Notification, ThreadModel, MessageModel

# Register your models here.
admin.site.register(Notification)
admin.site.register(ThreadModel)
admin.site.register(MessageModel)