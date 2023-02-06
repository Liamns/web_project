from django.db import models
from user.models import User
from event.models import BaseModel, image_upload_to

from django.db.models import UniqueConstraint



class Post(BaseModel):
    UPLOAD_PATH = "post-upload"

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자")
    post_img = models.ImageField(upload_to=image_upload_to, null=True, blank=True)
    view_cnt = models.SmallIntegerField(default=0)


    class Meta:
        ordering = ['-created_at']

class PostCount(models.Model):
    ip = models.CharField(max_length=30)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.ip

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="내용")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="등록일자")
    modified_at = models.DateTimeField(auto_now=True, verbose_name="수정일자")
    parent_comment_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

