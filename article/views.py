from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from article.models import Article
from article.serializers import ArticleSerializer, ArticleCreateSerializer
from rest_framework import status
from pathlib import Path
from .serializers import BookmarkSerializer
from .models import Bookmark
import json
import os


# BASE_DIR = Path(__file__).resolve().parent.parent
# secret_file = os.path.join(BASE_DIR,'api_key.json')

# with open(secret_file) as f:
#     secrets = json.loads(f.read())


# def get_secret(setting, secrets=secrets):
#     try:
#         return secrets[setting]
#     except KeyError:
#         error_msg = "Set the {} environment variable".format(setting)
#         raise error_msg
    

class ArticleView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
# 작성자 : 공민영
# 내용 : 모든 게시글 가져오기
# 최초 작성일 : 2023.06.08
# 업데이트 일자 : 2023.06.08
    def get(self, request):
        article = Article.objects.all().order_by('-created_at')
        serializer = ArticleSerializer(article, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# 작성자 : 공민영
# 내용 : 게시글 작성하기
# 최초 작성일 : 2023.06.08
# 업데이트 일자 : 2023.06.08
    def post(self, request):
        serializer = ArticleCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

  
class ArticleDetailView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
# 작성자 : 공민영
# 내용 : 게시글 상세보기
# 최초 작성일 : 2023.06.08
# 업데이트 일자 : 2023.06.08
    def get(self, request, user_id):
        article = Article.objects.get(id = user_id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# 작성자 : 공민영
# 내용 : 게시글 수정하기
# 최초 작성일 : 2023.06.08
# 업데이트 일자 : 2023.06.08
    def put(self, request, user_id):
        article = Article.objects.get(id = user_id)
        # 본인이 작성한 게시글이 맞다면
        if request.user == article.user:
            serializer = ArticleCreateSerializer(article, data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # 본인의 게시글이 아니라면
        else:
            return Response({'message':'로그인 후 이용해주세요.'}, status=status.HTTP_403_FORBIDDEN)
    
# 작성자 : 공민영
# 내용 : 게시글 삭제하기
# 최초 작성일 : 2023.06.08
# 업데이트 일자 : 2023.06.08
    def delete(self, request, user_id):
        article = Article.objects.get(id=user_id)
        # 본인이 작성한 게시글이 맞다면
        if request.user == article.user:
            article.delete()
            return Response({'message':'게시글이 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
        # 본인의 게시글이 아니라면
        else:
            return Response({'message':'본인 게시글만 삭제 가능합니다.'}, status=status.HTTP_403_FORBIDDEN)

class BookmarkCreate(generics.CreateAPIView):
# 작성자 : 마동휘
# 내용 : 북마크
# 최초 작성일 : 2023.06.12
# 업데이트 일자 : 2023.06.13
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        from user.serializers import UserSerializer
        return UserSerializer
    
class BookmarkDelete(generics.DestroyAPIView):
# 작성자 : 마동휘
# 내용 : 북마크
# 최초 작성일 : 2023.06.12
# 업데이트 일자 : 2023.06.13
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]