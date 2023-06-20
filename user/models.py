from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.urls import reverse
import re
from rest_framework.serializers import ValidationError

def check_password(password):
    password_regex = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&^])[A-Za-z\d$@$!%*#?&^]{8,}$"
    if not re.match(password_regex, password):
        raise ValidationError('8자 이상의 영문 대/소문자, 숫자, 특수문자 조합이어야 합니다!')
    return password
class UserManager(BaseUserManager):
    '''
    작성자 : 이준영
    내용 : 일반계정, 슈퍼계정 생성
    최초 작성일 : 2023.06.09
    업데이트 일자 : 2023.06.14
    '''
    def create_user(self, email, nickname, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            nickname=nickname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password=None):
        user = self.create_user(
            email,
            nickname=nickname,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
class User(AbstractBaseUser, PermissionsMixin):
    '''
    작성자 : 이준영
    내용 : sns가입자도 통합
    최초 작성일 : 2023.06.09
    업데이트 일자 : 2023.06.14
    '''
    GENDERS = [
        ("M", "Male"),
        ("F", "Female"),
    ]
    email = models.EmailField("이메일", max_length=255, unique=True)
    nickname = models.CharField("닉네임", max_length=50)
    profile_image = models.CharField("프로필_이미지", max_length=255, null=True, blank=True)
    password = models.CharField("비밀번호", max_length=256)    
    sns_id = models.PositiveIntegerField("sns고유번호", null=True, blank=True)    
    access_token = models.CharField("접근토큰", max_length=255, null=True, blank=True)
    expires_in = models.CharField("접근토큰_만료시간", max_length=255, null=True, blank=True)
    refresh_token = models.CharField("갱신토큰", max_length=255, null=True, blank=True)
    refresh_token_expires_in = models.CharField("갱신토큰_만료시간", max_length=255, null=True, blank=True)
    
    age = models.PositiveIntegerField("나이", null=True)
    gender = models.CharField("성별", max_length=1, choices=GENDERS, null=True, blank=True)
    created_at = models.DateTimeField("생성시각", auto_now_add=True)
    updated_at = models.DateTimeField("수정시각", auto_now=True)
    followings = models.ManyToManyField("self", symmetrical=False, related_name="followers", blank=True)
    followings = models.ManyToManyField("self", symmetrical=False, related_name="followers", blank=True)
    # """
    # symmetrical : 대칭여부설정 Ture라면 자동 맞팔, False라면 한쪽만 팔로우
    # """
    LOGIN_TYPES = [
        ("normal", "일반"),
        ("kakao", "카카오"),
        ("google", "구글"),
        ("naver", "네이버"),
    ]
    login_type = models.CharField(
        "로그인유형", max_length=10, choices=LOGIN_TYPES, default="normal"
    )

    is_active = models.BooleanField("활성화여부", default=True)
    is_admin = models.BooleanField("관리자여부", default=False)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname"]

    def __str__(self):
        return self.nickname

    def get_absolute_url(self):
        return reverse("profile_view", kwargs={"user_id": self.pk})
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20)
    profile_image = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.nickname
