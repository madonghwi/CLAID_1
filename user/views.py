import requests, traceback

from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.core.mail import send_mail
from django.contrib import messages

from user.models import User, Profile
from user.tokens import account_activation_token
from user.serializers import UserSerializer, SNSUserSerializer, MyTokenObtainPairSerializer, CustomTokenObtainPairSerializer, ProfileSerializer

from CLAID.settings import SOCIAL_OUTH_CONFIG

from article.models import Article

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication, TokenError, InvalidToken
from rest_framework.generics import get_object_or_404

GOOGLE_API_KEY = SOCIAL_OUTH_CONFIG['GOOGLE_API_KEY']

'''
작성자 : 이준영
내용 : KAKAO_KEYS
최초 작성일 : 2023.06.14
'''
KAKAO_REST_API_KEY = SOCIAL_OUTH_CONFIG['KAKAO_REST_API_KEY']
KAKAO_REDIRECT_URL = SOCIAL_OUTH_CONFIG['KAKAO_REDIRECT_URL']
KAKAO_SECRET_KEY = SOCIAL_OUTH_CONFIG['KAKAO_SECRET_KEY']
KAKAO_ADMIN_KEY = SOCIAL_OUTH_CONFIG['KAKAO_ADMIN_KEY']
KAKAO_LOGOUT_REDIRECT_URL = SOCIAL_OUTH_CONFIG['KAKAO_LOGOUT_REDIRECT_URL']

class UserSignupView(APIView):
    permission_classes = [AllowAny]
    '''
    작성자 : 공민영
    내용 : 회원가입
    최초 작성일 : 2023.06.08
    업데이트 일자 : 2023.06.08
    '''
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "인증메일을 발송했습니다."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    '''
    작성자 : 공민영
    내용 : 로그인
    최초 작성일 : 2023.06.08
    업데이트 일자 : 2023.06.08
    '''
    serializer_class = MyTokenObtainPairSerializer


class UserActivate(APIView):
    permission_classes = [AllowAny]
    '''
    작성자 : 공민영
    내용 : 이메일 인증 링크 클릭시
    최초 작성일 : 2023.06.08
    업데이트 일자 : 2023.06.08
    '''
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
                return HttpResponse("이메일 인증이 완료되었습니다. 로그인이 가능합니다!")
            else:
                return Response({"message":"만료된 토큰"}, status=status.HTTP_408_REQUEST_TIMEOUT)
        
        except Exception as e:
            print(traceback.format_exc())
            return Response({"message": "에러가 발생했습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserLogoutView(APIView):
    '''
    작성자 : 공민영
    내용 : 로그아웃
    최초 작성일 : 2023.06.08
    업데이트 일자 : 2023.06.08
    '''
    def post(self, request):
        response = Response({"message": "로그아웃 완료"}, status=status.HTTP_200_OK)
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        return response
    
    
class KakaoCallBackView(APIView):
    '''
    작성자 : 이준영
    내용 : 프론트에서 받은 카카오 code를 받아 최종으로 JWT 토큰을 받으며 로그인
    최초 작성일 : 2023.06.14
    '''
    permission_classes = [AllowAny]
    
    def get(self, request):
        '''
        작성자 : 이준영
        내용 : 카카오 code를 받아 카카오 Token을 받는다.
        최초 작성일 : 2023.06.14
        '''
        code = request.GET.get('code')
        kakao_token_api = 'https://kauth.kakao.com/oauth/token'
        data = {
            'grant_type' : 'authorization_code',
            'client_id' : KAKAO_REST_API_KEY,
            'redirection_url' : KAKAO_REDIRECT_URL,
            'code' : code,
            'client_secret' : KAKAO_SECRET_KEY,
        }
        headers = {'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'}        
        token_response = requests.post(kakao_token_api, data=data, headers=headers)        
        
        access_token = token_response.json().get('access_token')
        expires_in = token_response.json().get('expires_in')
        refresh_token = token_response.json().get('refresh_token')
        refresh_token_expires_in = token_response.json().get('refresh_token_expires_in')
        
        print(access_token)
        '''
        작성자 : 이준영
        내용 : 카카오 Token으로 사용자 정보를 받고,
        신규, 기존 사용자를 식별하여
        카카오 Token과 정보를 DB에 저장
        최초 작성일 : 2023.06.14
        '''
        user_data = requests.post(
            "https://kapi.kakao.com/v2/user/me",
            headers={
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
                    "Authorization": f"Bearer {access_token}",
                    # "Access-Control-Allow-Origin": "http://127.0.0.1:5500/kakao.html",
            },
        )
        
        user_data = user_data.json()

        email = user_data.get("kakao_account").get("email")
        sns_id = user_data.get('id')
        nickname = user_data.get('properties').get('nickname')
        profile_image = user_data.get('properties').get('profile_image')
        
        kakao_data  = {
            "email" : email,
            "login_type": "kakao",
            "sns_id" : sns_id,
            "nickname" : nickname,
            "profile_image" : profile_image,
            "access_token" : access_token,
            "expires_in" : expires_in,
            "refresh_token" : refresh_token,
            "refresh_token_expires_in" : refresh_token_expires_in,
        }
        
        try:
            kakao_user, created = User.objects.get_or_create(email=email, defaults=kakao_data)
            if created:
                message = "신규 유저 정보 생성!"
                response_status = status.HTTP_200_OK
            else:
                serializer = SNSUserSerializer(kakao_user, data=kakao_data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    message = "기존 유저 정보 업데이트!"
                    response_status = status.HTTP_200_OK
                else:
                    return Response({"message": {serializer.errors}}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "DB 저장 오류입니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        '''
        작성자 : 이준영
        내용 : 사용자 정보로 JWT Token을 만들어 커스텀해서 보내줌.
        최초 작성일 : 2023.06.14
        '''
        kakao_user = User.objects.get(email=email)
        
        token = MyTokenObtainPairSerializer.get_token(kakao_user)
        
        # JWT 토큰을 문자열로 변환
        access_token = str(token.access_token)        
        refresh_token = str(token)

        # OpenID connect 사용해요?

        # 오류 등을 try 로 나누고 return이나 response도 나누기
        
        # response에 답기
        response_data = {'message': message, 'access_token': access_token, 'refresh_token': refresh_token}
        return Response(response_data, status=response_status)

class KakaoLogoutView(APIView):
    '''
    작성자 : 이준영
    내용 : JWT Token을 받고 request의 email로 DB의 kakao token을 찾아 요청을 보내
    kakao token 만료를 시키고 DB의 kakao token 삭제하는 보안 작업
    최초 작성일 : 2023.06.15
    '''
    permission_classes = [IsAuthenticated]    
    def post(self, request):
        user = get_object_or_404(User, email=request.user.email)
        
        access_token = user.access_token
        
        # 로그아웃 (DB에 저장한 access_token을 사용한)
        # 로그아웃 되면 토큰이 만료됨.
        headers = {"Authorization": f'Bearer {access_token}'}
        logout_response = requests.post('https://kapi.kakao.com/v1/user/logout', headers=headers)
        
        if logout_response.status_code == 200:
            # + 카카오의 접근토큰 삭제
            user.access_token = None
            # 토큰 만료시간도 해야하나?
            user.save()
            return Response({"message" : "로그아웃 되셨습니다."}, status=status.HTTP_200_OK)
        elif logout_response.status_code == 401:
            return Response({"message" : "토큰이 유효하지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        elif logout_response.status_code == 400:
            return Response({"message" : "잘못된 요청입니다. 관리자에게 문의하세요."}, status=status.HTTP_400_BAD_REQUEST)
        else:                            
            return Response({"message" : "서버 오류가 발생했습니다. 관리자에게 문의하세요."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class KakaoUserView(APIView):
    '''
    작성자 : 이준영
    내용 : KAKAO_ADMIN_KEY로 Kakao 고유 id를 써서 Kakao DB의 사용자 정보 가져오기
    최초 작성일 : 2023.06.15
    '''
    permission_classes = [AllowAny]
    def get(self, request, sns_id):
        response = requests.post(
            "https://kapi.kakao.com/v2/user/me",
            data={
                "target_id_type" : "user_id",
                "target_id" : sns_id, 
            },
            headers={
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
                    "Authorization": f"KakaoAK {KAKAO_ADMIN_KEY}",
                    # "Access-Control-Allow-Origin": "http://127.0.0.1:5500/kakao.html",
            },
        )  
        
        if response.status_code == 200:
            user_data = response.json()            
            data = {            
            # "sns_id" : user_data.get("id"),
            "profile_image": user_data.get("properties").get("profile_image"),
            "email": user_data.get("kakao_account").get("email"),
            "nickname": user_data.get("properties").get("nickname"),
            # "gender": user_data.get("properties").get("gender"),
            # "login_type": "kakao",
        }    
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Kakao API 요청에 실패했습니다."}, status=response.status_code)
        
class KakaoUnLinkView(APIView):
    '''
    작성자 : 이준영
    내용 : JWT Token으로 접속한 Kakao user의 request.user.email로 DB의 Kakao access_token을 찾아 Kakao access_token으로 연결 끊기
    최초 작성일 : 2023.06.15
    '''
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = get_object_or_404(User, email=request.user.email)        
        access_token = user.access_token        
        
        # 연결한 정보들 삭제 할 지 추후 회의를 해야함.
        
        headers = {
            "Content-Type": "application/x--www-form-urlencoded",
            "Authorization": f'Bearer {access_token}'
            }
        response = requests.post('https://kapi.kakao.com/v1/user/unlink', headers=headers)
        if response.status_code == 200:
            return Response({"message" : "연결 끊기에 성공하였습니다."}, status=status.HTTP_200_OK)
        else:
            return Response({"message" : "토큰이 유효하지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        

'''
작성자 : 왕규원
내용 : FOLLOW
최초 작성일 : 2023.06.16
'''
class FollowView(APIView):
    def post(self, request, user_id):
        following = get_object_or_404(User, id=user_id)
        follower = request.user
        if follower in following.followers.all():
            following.followers.remove(follower)
            return Response("팔로우를 취소하였습니다.", status=status.HTTP_200_OK)
        else :
            following.followers.add(follower)
            return Response("팔로우하였습니다.", status=status.HTTP_200_OK)


class GoogleLogin(APIView):
    '''
    작성자 :김은수
    내용 : 구글 로그인
    최초 작성일 : 2023.06.12
    업데이트 일자 : 2023.06.13
    '''  
    permission_classes = [AllowAny]
    def get(self, request):
        return Response(GOOGLE_API_KEY, status=status.HTTP_200_OK)
    
    def post(self, request):
        access_token = None
        print(request.data)
        if request.data["access_token"]:
            access_token = request.data["access_token"]
        else:
            return Response({'msg':'google access_token 받아오지 못함'})
        print(access_token)
        '''
        작성자 :김은수
        내용 : 구글 oauth2 서버에 요청해서 유저정보 받아오기,
        받을 수 있는 유저 정보 : id, email, verified_email, name, given_name, picture, locale
        최초 작성일 : 2023.06.16
        업데이트 일자 : 2023.06.16
        '''
        # google_answer_url = request.data["params"]
        # print(f'구글 url{google_answer_url}')
        user_data = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        
        user_data = user_data.json()
        
        email = user_data.get("email")


        data = {
            "profile_image": user_data.get("picture"),
            "email": email,
            "nickname": user_data.get("name"),
            # "login_type": "google",
        }
        
        try:
            google_user, created = User.objects.get_or_create(email=email, defaults=data)
            if created:
                message = "신규 유저 정보 생성!"
                response_status = status.HTTP_200_OK               
            else:
                serializer = SNSUserSerializer(google_user, data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    message = "기존 유저 정보 업데이트!"
                    response_status = status.HTTP_200_OK
                else:
                    return Response({"message": {serializer.errors}}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "DB 저장 오류입니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        refresh = RefreshToken.for_user(google_user)
        access_token = MyTokenObtainPairSerializer.get_token(google_user)

        return Response(
                {'message': message, "refresh_token": str(refresh), "access_token": str(access_token.access_token)},
                status=response_status,
            )

class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        if request.user.login_type == 'sns':
            serializer = SNSUserSerializer(request.user)
        else:
            serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        data = {
            "nickname": request.data.get("nickname", profile.nickname),
            "profile_image": request.data.get("profile_image", profile.profile_image)
        }
        profile_serializer = ProfileSerializer(profile, data=data, partial=True)
        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response(profile_serializer.data)
        return Response(profile_serializer.errors, status=400)
    
    def dispatch(self, request, *args, **kwargs):
        try:
            self._jwt_authenticate(request)
        except TokenError as e:
            return self._handle_invalid_token(e)
        return super().dispatch(request, *args, **kwargs)
    
    def _jwt_authenticate(self, request):
        auth = JWTAuthentication()
        return auth.authenticate(request)

    def _handle_invalid_token(self, error):
        if isinstance(error, InvalidToken):
            return Response({"error": "유효하지 않은 액세스 토큰입니다."}, status=401)
        return Response({"error": "토큰 오류 발생"}, status=401)
