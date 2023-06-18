
from django.shortcuts import render
# Create your views here.
from rest_framework import generics
from rest_framework import mixins

from article.models import Comment
from article.serializers import CommentSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from article.models import Article, HitsCount, get_client_ip
from datetime import datetime, timedelta
from django.utils import timezone
from article.serializers import ArticleSerializer, ArticleCreateSerializer
from rest_framework import status
from pathlib import Path

import django
import json
import os


# BASE_DIR = Path(__file__).resolve().parent.parent
# secret_file = os.path.join(BASE_DIR,'api_key.json')

BASE_DIR = Path(__file__).resolve().parent.parent
secret_file = os.path.join(BASE_DIR,'.env')


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
    '''
    작성자 : 공민영
    내용 : 모든 게시글 가져오기
    최초 작성일 : 2023.06.08
    업데이트 일자 : 2023.06.08
    '''
    def get(self, request):
        article = Article.objects.all().order_by('-created_at')
        serializer = ArticleSerializer(article, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    '''    
    작성자 : 공민영
    내용 : 게시글 작성하기
    최초 작성일 : 2023.06.08
    업데이트 일자 : 2023.06.08
    '''
    def post(self, request):
        serializer = ArticleCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

  
class ArticleDetailView(APIView):
    queryset = Article.objects.all().order_by('-pk')
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    '''    
    작성자 : 공민영
    내용 : 게시글 상세보기
    최초 작성일 : 2023.06.08
    최종 수정자 : 이준영
    수정내용 : 오류 시 404가 나오게 바꿈, put 메시지 수정
    nickname 추가
    업데이트 일자 : 2023.06.17
    '''
    def get(self, request, article_id):
        article = get_object_or_404(Article, id = article_id)
        serializer = ArticleSerializer(article)
        '''
        작성자 :왕규원
        내용 : 조회수 기능 및 ip 중복방지 기능
        최초 작성일 : 2023.06.13
        업데이트 일자 : 2023.06.15
        '''
        ip = get_client_ip(request)
        expire_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)  # 다음 날 자정을 만료 날짜로 설정
        cnt = HitsCount.objects.filter(ip=ip, article=article, expire_date__gt=timezone.now()).count() # 만료 기간 >= 현재시간, 즉 아직 만료 되지 않은 경우를 count
        if cnt == 0:  #만료가 됐다 = article_hitscount 테이블에 없는 경우
            article.click
            hc = HitsCount(ip=ip, article=article, expire_date=expire_date)
            hc.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.data, status=status.HTTP_200_OK)
    '''       
    작성자 : 공민영
    내용 : 게시글 수정하기
    최초 작성일 : 2023.06.08
    업데이트 일자 : 2023.06.08
    '''
    def patch(self, request, article_id):
            article = get_object_or_404(Article, id = article_id)
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
                return Response({'message':'본인 게시글만 수정 가능합니다.'}, status=status.HTTP_403_FORBIDDEN)

    '''
    작성자 : 공민영
    내용 : 게시글 삭제하기
    최초 작성일 : 2023.06.08
    업데이트 일자 : 2023.06.08
    '''
    def delete(self, request, article_id):
            article = get_object_or_404(Article, id = article_id)
                # 본인이 작성한 게시글이 맞다면
            if request.user == article.user:
                article.delete()
                return Response({'message':'게시글이 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
                # 본인의 게시글이 아니라면
            else:
                return Response({'message':'본인 게시글만 삭제 가능합니다.'}, status=status.HTTP_403_FORBIDDEN)
        


class CommentView(generics.ListCreateAPIView):
    '''
    작성자 :김은수
    내용 : 댓글의 생성과 조회가 가능함
    최초 작성일 : 2023.06.08
    업데이트 일자 : 2023.06.09
    '''
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    

class CommentViewByArticle(generics.RetrieveUpdateDestroyAPIView):
    '''
    작성자 :김은수
    내용 : 댓글의 수정과 삭제가 가능함
    최초 작성일 : 2023.06.07
    업데이트 일자 : 2023.06.09
    '''  
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class ArticleGoodView(APIView):
    def post(self,request,article_id):
        article = get_object_or_404(Article, id=article_id)
        if request.user in article.good.all():
            article.good.remove(request.user)
            return Response("좋아요를 취소하였습니다.", status=status.HTTP_200_OK)
        else:
            article.good.add(request.user)
            return Response("좋아요를 눌렀습니다.", status=status.HTTP_200_OK)
        

class CommentGoodView(APIView):
    def post(self,request,comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user in comment.good.all():
            comment.good.remove(request.user)
            return Response("좋아요를 취소하였습니다.", status=status.HTTP_200_OK)
        else:
            comment.good.add(request.user)
            return Response("좋아요를 눌렀습니다.", status=status.HTTP_200_OK)