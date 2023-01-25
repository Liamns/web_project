from django.db import models

# Create your models here.


class GenericFileUpload(models.Model):
    file_upload = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.file_upload}'
    