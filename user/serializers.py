from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from user.models import User
from article.models import Article
from django.core.mail import EmailMessage
from CLAID import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from user.tokens import account_activation_token



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

        message = render_to_string("email_signup_message.html", {
            "user":user,
            "domain":"localhost:8000",
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
        })

        subject = "회원가입 인증 메일입니다."
        to = [user.email]
        from_email = settings.DEFAULT_FROM_EMAIL
        EmailMessage(subject=subject, body=message, to=to, from_email=from_email).send()
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
# 작성자 : 공민영
# 내용 : 토큰
# 최초 작성일 : 2023.06.08
# 업데이트 일자 : 2023.06.08
    def get_token(cls, user):
        token = super().get_token(user)
        token["id"] = user.id
        token["email"] = user.email
        token["username"] = user.username
        token["is_active"] = user.is_active

        return token