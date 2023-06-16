from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import re
from rest_framework.serializers import ValidationError

def check_password(password):
    password_regex = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&^])[A-Za-z\d$@$!%*#?&^]{8,}$"
    if not re.match(password_regex, password):
        raise ValidationError('8자 이상의 영문 대/소문자, 숫자, 특수문자 조합이어야 합니다!')
    return password

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save()
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=40, null=True, blank=True)
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    password = models.CharField(max_length=100, validators=[check_password])
    is_subscribe = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=40, null=True, blank=True)
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    def __str__(self):
        return self.user.email
    
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
# class Point(TimeStampModel):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     claid = models.IntegerField()

#     class Meta :
#         db_table = 'point'

