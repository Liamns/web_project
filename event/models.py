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
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="등록일자")
    modified_at = models.DateTimeField(auto_now=True, verbose_name="수정일자")
    tags = TaggableManager(verbose_name="태그")
    location_tags = models.CharField(verbose_name="지역태그", max_length=128)
    content = models.TextField(default="", verbose_name="내용")
    title = models.CharField(max_length=256, verbose_name="제목")

    class Meta:
        abstract = True

def image_upload_to(instance, fileName):

    ext = fileName.split('.')[-1]
    return os.path.join(instance.UPLOAD_PATH, "%s.%s" % (uuid.uuid4(), ext))


class Event(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자")
    deadline = models.DateTimeField(verbose_name="마감날짜")
    participants_limit = models.SmallIntegerField(verbose_name="참여인원 제한 수")
    start_event = models.CharField(verbose_name="이벤트 시작일", max_length=50)
    end_event = models.CharField(verbose_name="이벤트 종료일", max_length=50)
    event_imgage = models.ImageField(upload_to=image_upload_to)
    EVENT_CATEGORY = [("운동","운동"), ("여행","여행"), ("문화관람","문화관람"), ("게임","게임"), ("음악","음악"), ("사교/인맥","사교/인맥"), ("봉사","봉사"), ("자유주제","자유주제")]
    category = models.CharField(max_length=20, choices=EVENT_CATEGORY, default="자유주제")


    class Meta:
        ordering = ['-created_at']



    
        
class Participants(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

