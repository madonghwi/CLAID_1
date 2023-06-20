from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers
from user.models import User, Profile

from article.models import Article
from django.core.mail import EmailMessage
from CLAID import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from user.tokens import account_activation_token


    
# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         token["email"] = user.email
#         token["login_type"] = user.login_type
#         return token


class SNSUserSerializer(serializers.ModelSerializer):
    '''
    작성자 : 이준영
    내용 : 일반 로그인 기능 구현 전 sns 로그인
    최초 작성일 : 2023.06.14
    '''
    class Meta:
        model = User
        fields = "__all__"
    
    def create(self, validated_data):        
        user = super().create(validated_data)
        user.save()        
        return user
    
    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
    # 작성자 : 공민영
    # 내용 : 회원가입
    # 최초 작성일 : 2023.06.08
    # 업데이트 일자 : 2023.06.08

    def create(self, validated_data):
        user = super().create(validated_data)
        user.is_active = False
        password = user.password
        # 비밀번호 암호화
        user.set_password(password)
        user.save()

        message = (
        "안녕하세요, {nickname}님!\n\n"
        "회원가입 인증을 완료하려면 다음 링크를 클릭해주세요:\n"
        "http://{domain}/user/activate/{uid}/{token}\n\n"
        "---\n"
        "감사합니다!"
        ).format(
            nickname=user.nickname,
            domain="localhost:8000",
            uid=urlsafe_base64_encode(force_bytes(user.pk)),
            token=account_activation_token.make_token(user),
        )

        subject = "회원가입 인증 메일입니다."
        to = [user.email]
        from_email = settings.DEFAULT_FROM_EMAIL
        EmailMessage(subject=subject, body=message, to=to, from_email=from_email).send()
        return user

    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    '''
    작성자 : 공민영
    내용 : 토큰
    최초 작성일 : 2023.06.08
    수정자 : 이준영
    내용 : 커스텀 토큰 페이로드 추가
    업데이트 일자 : 2023.06.14
    '''
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["id"] = user.id
        token["email"] = user.email
        token["login_type"] = user.login_type
        token["sns_id"] = user.sns_id
        token["nickname"] = user.nickname
        token["profile_image"] = str(user.profile_image)
        token["is_active"] = user.is_active
        return token
    
    def get_user(self, validated_data):
        user = self.user
        return user
    

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['nickname', 'profile_image']

