from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, BaseUserManager, PermissionsMixin
from allauth.account.models import EmailAddress

from django.dispatch import receiver
from django.db.models.signals import post_save

from message.models import GenericFileUpload
from django.utils import timezone


# AbstracUser
# AbstractBaseUser 상속

# 프로젝트에 필요한 user
# email 필드 == id 개념 == username 
# nickname, birth, address 추가

class UserManager(BaseUserManager):
    def _create_user(self, email, password, name, nickname, birth, address, **extra_fields):
        """
        Create and save a user with the given email, password, name.
        """
        if not email:
            raise ValueError("The given email must be set")

        email = self.normalize_email(email)

        user = self.model(email=email, name=name, nickname=nickname, birth=birth, address=address,  **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, name, nickname, birth, address, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, name, nickname, birth, address, **extra_fields)

    def create_superuser(self, email, password, name, nickname=None, birth=None, address=None, **extra_fields):
        """
        admin 계정에 nickname, birth, address 필요없음
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, name, nickname, birth, address, **extra_fields)
    

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User 생성 : AbstractUser or AbstractBaseUser 상속
    필드 추가 : email, password, name, nickname, birth, address

    권한 여부 추가
    """

    # null = True 지정하지 않으면 not null + unique ==> pk 속성
    email = models.EmailField(verbose_name="이메일", max_length=255, unique=True)
    password = models.CharField(verbose_name="비밀번호", max_length=128)
    name = models.CharField(verbose_name="이름", max_length=64)
    nickname = models.CharField(verbose_name="닉네임", max_length=50)
    birth = models.CharField(verbose_name="생년월일", max_length=20)
    address = models.CharField(verbose_name="거주지역", max_length=128)
    is_staff = models.BooleanField(verbose_name="관리자여부", default=False)
    is_active = models.BooleanField(verbose_name="활성화여부", default=True)

    # CustomUser 를 기반으로 user 생성을 도와줄 매니저 클래스 등록
    objects = UserManager()  # User.objects.create_user() 생성

    # username(아이디) 으로 사용할 필드 지정
    USERNAME_FIELD = "email"
#
    # email, password 요소 외에 사용자 생성 시 꼭 받아야하는 필드 작성
    REQUIRED_FIELDS = ["name", "nickname", "birth", "address"]

    # def is_active(self):
    #     return self.email_address.verified

    def __str__(self) -> str:
        return "<%s>" % (self.email)

class Profile(models.Model):
    """
    회원가입 시 무조건 같이 실행
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="회원")
    profile_img = models.ImageField(upload_to="profile/", default="profile/default.png", verbose_name="프로필이미지")
    participations_cnt = models.SmallIntegerField(verbose_name="참여횟수", default=0)
    post_cnt = models.SmallIntegerField(verbose_name="게시글 수", default=0)
    comment_cnt = models.SmallIntegerField(verbose_name="댓글 수", default=0)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    def __str__(self) -> str:
        return "<%s>" % (self.user)
    

class Favorite(models.Model):
    user = models.OneToOneField(User, related_name="user_favorites", on_delete=models.CASCADE)
    favorite = models.ManyToManyField(User, related_name="user_favoured")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}"

    class Meta:
        ordering = ("created_at",)