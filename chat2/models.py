from django.db import models

# Create your models here.


from datetime import datetime

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    

class Message(models.Model):
    value = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.CharField(max_length=100)
    room = models.CharField(max_length=100)
    