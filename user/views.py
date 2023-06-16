from django.shortcuts import render

# Create your views here.
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from user.serializers import UserSerializer, MyTokenObtainPairSerializer
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from user.tokens import account_activation_token
import traceback
from django.shortcuts import redirect, render
from .models import User
from article.models import Article
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import send_mail


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # 로그인 성공 시 리디렉션될 URL
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

class UserSignupView(APIView):
# 작성자 : 공민영
# 내용 : 회원가입
# 최초 작성일 : 2023.06.08
# 업데이트 일자 : 2023.06.08
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "인증메일을 발송했습니다."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
# 작성자 : 공민영
# 내용 : 로그인
# 최초 작성일 : 2023.06.08
# 업데이트 일자 : 2023.06.08
    serializer_class = MyTokenObtainPairSerializer


class UserActivate(APIView):
    permission_classes = [AllowAny]
# 작성자 : 공민영
# 내용 : 이메일 인증
# 최초 작성일 : 2023.06.08
# 업데이트 일자 : 2023.06.08
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(User, pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user=None

        try:
            if user is not None and account_activation_token.check_token(user, token):
                user.is_active = True
                user.save()
                return redirect('user:success')
            else:
                return Response({"message":"만료된 토큰"}, status=status.HTTP_408_REQUEST_TIMEOUT)
        
        except Exception as e:
            print(traceback.format_exc())

# 작성자 : 공민영
# 내용 : 이메일 성공시
# 최초 작성일 : 2023.06.08
# 업데이트 일자 : 2023.06.08
def active_success(request):
    return render(request, "email_active.html")



class UserLogoutView(APIView):
# 작성자 : 공민영
# 내용 : 로그아웃
# 최초 작성일 : 2023.06.08
# 업데이트 일자 : 2023.06.08
    def post(self, request):
        response = Response({"message": "로그아웃 완료"}, status=status.HTTP_200_OK)
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        return response