from django.contrib import admin

# Register your models here.
from .models import Event, EventImage, Participants

class EventAdmin(admin.ModelAdmin):
    list_display = ('user','created_at')

admin.site.register(Event, EventAdmin)
admin.site.register(EventImage)
admin.site.register(Participants)