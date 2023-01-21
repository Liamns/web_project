from django.db import models
from user.models import User
from event.models import BaseModel, image_upload_to

from django.db.models import UniqueConstraint



class Post(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자")
    view_cnt = models.SmallIntegerField()


    class Meta:
        ordering = ['-created_at']

class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="댓글")
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="댓글")
    content = models.TextField()

class PostImage(models.Model):
    UPLOAD_PATH = "post-upload"

    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="작성글")
    post_img = models.ImageField(upload_to=image_upload_to)
    order = models.SmallIntegerField()

    class Meta:
        constraints = [UniqueConstraint(name='unique_together', fields=['post','order'])]
        ordering = ['order']

