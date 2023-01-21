from django.db import models
from user.models import User

import os
import uuid
from django.db.models import UniqueConstraint
from taggit.managers import TaggableManager

# contents - 작성날짜, 수정날짜, 태그, 장소태그, 내용, 제목
class BaseModel(models.Model):
    """
    추상클래스
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="등록날짜")
    modified_at = models.DateTimeField(auto_now=True, verbose_name="수정날짜")
    tags = TaggableManager(verbose_name="태그")
    location_tags = TaggableManager(verbose_name="지역태그")
    content = models.TextField(default="", verbose_name="내용")
    title = models.CharField(max_length="256", verbose_name="제목")

    class Meta:
        abstract = True

class Event(BaseModel):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자")
    deadline = models.DateTimeField(verbose_name="마감날짜")
    participants_limit = models.SmallAutoField(verbose_name="참여인원 제한 수")
    participants_cnt = models.SmallIntegerField(verbose_name="참여인원 수")
    start_event = models.DateTimeField(verbose_name="이벤트 시작일")
    end_event = models.DateTimeField(verbose_name="이벤트 종료일")


    class Meta:
        ordering = ['-created_at']

def image_upload_to(instance, fileName):

    ext = fileName.split('.')[-1]
    return os.path.join(instance.UPLOAD_PATH, "%s.%s" % (uuid.uuid4(), ext))

class EventImage(models.Model):
    UPLOAD_PATH = "event-upload"

    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="작성글")
    event_img = models.ImageField(upload_to=image_upload_to)
    order = models.SmallIntegerField()

    class Meta:
        constraints = [UniqueConstraint(name='unique_together', fields=['event','order'])]
        ordering = ['order']
