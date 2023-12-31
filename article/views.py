
from django.shortcuts import render
# Create your views here.
from rest_framework import generics
from rest_framework import mixins

from article.models import Comment, NoticeHitsCount
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from article.models import Article, VocalNotice, HitsCount, get_client_ip,NoticeComment
from user.models import User, Point, PointHistory
from datetime import datetime, timedelta
from django.utils import timezone
from article.serializers import ArticleSerializer, ArticleCreateSerializer, VocalNoticeSerializer, VocalNoticeCreateSerializer
from article.serializers import CommentUserSerializer, UserIdSerializer,CommentSerializer, CommentCreateSerializer, NoticeCommentSerializer, NoticeCommentCreateSerializer
from pathlib import Path

import django
import json
import os

BASE_DIR = Path(__file__).resolve().parent.parent
secret_file = os.path.join(BASE_DIR,'.env')

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
    수정자 : 공민영
    수정내용 : 게시글 작성할 때 마다 포인트 지급, 이력 저장
    업데이트 일자 : 2023.07.02
    '''
    def post(self, request):
        serializer = ArticleCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)

            user = request.user
            user_point = Point.objects.get(user=user)

            user_point.points += 1000
            PointHistory.objects.create(user=user, point_change=+1000, reason="게시글 작성")
            user_point.save()

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
    수정자 : 이준영
    내용 : patch의 역할을 수행할 수 있게 수정함.
    수정일 : 2023.07.09
    '''
    def patch(self, request, article_id):
            article = get_object_or_404(Article, id = article_id)
                # 본인이 작성한 게시글이 맞다면
            if request.user == article.user:
                serializer = ArticleCreateSerializer(article, data=request.data, partial=True)
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
    수정자 : 공민영
    수정내용 : 게시글을 작성한지 24시간이 지나기 전 삭제시 포인트 차감, 이력 저장
    업데이트 일자 : 2023.07.02
    '''
    def delete(self, request, article_id):
            article = get_object_or_404(Article, id = article_id)
                # 본인이 작성한 게시글이 맞다면
            if request.user == article.user:
                if article.song or article.article_image:
                    article.song.delete()
                    article.article_image.delete()
                article.delete()

            user = request.user
            one_day_passed = timezone.now() > (article.created_at + timedelta(days=1))

            if not one_day_passed:
                user_point = Point.objects.get(user=request.user)
                user_point.points -= 1000
                PointHistory.objects.create(user=user, point_change=-1000, reason="게시글 삭제")
                user_point.save()
                
                return Response({'message':'게시글이 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
                # 본인의 게시글이 아니라면
            else:
                return Response({'message':'본인 게시글만 삭제 가능합니다.'}, status=status.HTTP_403_FORBIDDEN)
        


class CommentView(generics.ListCreateAPIView):
    # permission_classes = [AllowAny]
    permission_classes = [IsAuthenticatedOrReadOnly]
    '''
    작성자 :김은수
    내용 : 댓글의 생성과 조회가 가능함
    최초 작성일 : 2023.06.08
    업데이트 일자 : 2023.06.21
    수정자 : 공민영
    수정내용 : 댓글 작성할 때 마다 포인트 지급
    업데이트 일자 : 2023.07.02
    '''
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        article_id = self.kwargs['article_id']
        return Comment.objects.filter(article_id=article_id)

    def get(self, request, *args, **kwargs):
        article_id = self.kwargs['article_id']
        comments = Comment.objects.filter(article_id=article_id)
        comment_data = []
        
        for comment in comments:
            user = User.objects.get(id=comment.user_id)
            comment_good = comment.good.all()
            user_data = CommentUserSerializer(user).data
            serialzier = UserIdSerializer(comment_good, many=True)
            comment_data.append({
                'id': comment.id,
                'content':comment.content,
                'user': user_data,
                'good': serialzier.data
            })
        return Response(comment_data)
    
    def post(self, request, *args, **kwargs):
        serializer = CommentCreateSerializer(data=request.data)
        lookup_url_kwarg = 'article_id'
        article_id = self.kwargs.get(lookup_url_kwarg)
        article = Article.objects.get(id=article_id)

        if serializer.is_valid():
            serializer.save(user=request.user, article=article)

            user = request.user
            user_point = Point.objects.get(user=user)

            user_point.points += 500
            PointHistory.objects.create(user=user, point_change=+500, reason="댓글 작성")
            user_point.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentViewByArticle(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [AllowAny]
    permission_classes = [IsAuthenticatedOrReadOnly]
    '''
    작성자 :김은수
    내용 : 댓글의 수정과 삭제가 가능함
    최초 작성일 : 2023.06.07
    업데이트 일자 : 2023.06.09
    '''  
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer




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
    permission_classes = [AllowAny]
    def post(self,request,comment_id,article_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user in comment.good.all():
            comment.good.remove(request.user.id)
            return Response("해당 댓글에 좋아요를 취소하였습니다.", status=status.HTTP_200_OK)
        else:
            comment.good.add(request.user.id)
            return Response("해당 댓글에 좋아요를 눌렀습니다.", status=status.HTTP_200_OK)
            

# 방법공유
class VocalNoticeView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    '''
    작성자 : 공민영, 왕규원
    내용 : 보컬로이드 방법공유 게시글 가져오기
    최초 작성일 : 2023.06.19
    업데이트 일자 : 2023.06.19
    '''
    def get(self, request):
        article = VocalNotice.objects.all().order_by('-created_at')
        serializer = VocalNoticeSerializer(article, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    '''    
    작성자 : 공민영, 왕규원
    내용 : 보컬로이드 방법공유 게시글 작성하기
    최초 작성일 : 2023.06.19
    수정자 : 공민영
    수정내용 : 게시글 작성할 때 마다 포인트 지급, 이력 저장
    업데이트 일자 : 2023.07.02
    수정자 : 이준영
    내용 : 수정이 안되어 핫 픽스, models에 맞게 다시 수정
    수정일 : 2023.07.10
    '''
    def post(self, request):
        serializer = VocalNoticeCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)

            user = request.user
            user_point = Point.objects.get(user=user)

            user_point.points += 1000
            PointHistory.objects.create(user=user, point_change=+1000, reason="게시글 작성")
            user_point.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class VocalNoticeDetailView(APIView):
    queryset = VocalNotice.objects.all().order_by('-pk')
    serializer_class = VocalNoticeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    '''    
    작성자 : 공민영, 왕규원
    내용 : 보컬로이드 방법공유 게시글 상세보기
    최초 작성일 : 2023.06.19
    업데이트 일자 : 2023.06.19
    '''
    def get(self, request, article_id):
        article = get_object_or_404(VocalNotice, id = article_id)
        serializer = VocalNoticeSerializer(article)
        ip = get_client_ip(request)
        expire_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)  # 다음 날 자정을 만료 날짜로 설정
        cnt = NoticeHitsCount.objects.filter(ip=ip, article=article, expire_date__gt=timezone.now()).count() # 만료 기간 >= 현재시간, 즉 아직 만료 되지 않은 경우를 count
        if cnt == 0:  #만료가 됐다 = article_hitscount 테이블에 없는 경우
            article.click
            hc = NoticeHitsCount(ip=ip, article=article, expire_date=expire_date)
            hc.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.data, status=status.HTTP_200_OK)
    '''       
    작성자 : 공민영, 왕규원
    내용 : 보컬로이드 방법공유 게시글 수정하기
    최초 작성일 : 2023.06.19
    수정자 : 이준영
    내용 : 수정이 안되어 핫픽스, models에 맞게 다시 수정
    최초 작성일 : 2023.07.10
    '''
    def patch(self, request, article_id):
            article = get_object_or_404(VocalNotice, id = article_id)
                # 본인이 작성한 게시글이 맞다면
            if request.user == article.user:
                serializer = VocalNoticeCreateSerializer(article, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save(user=request.user)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                # 본인의 게시글이 아니라면
            else:
                return Response({'message':'본인 게시글만 수정 가능합니다.'}, status=status.HTTP_403_FORBIDDEN)

    '''
    작성자 : 공민영, 왕규원
    내용 : 보컬로이드 방법공유 게시글 삭제하기
    최초 작성일 : 2023.06.19
    수정자 : 공민영
    수정내용 : 게시글을 작성한지 24시간이 지나기 전 삭제시 포인트 차감, 이력 저장
    업데이트 일자 : 2023.07.02
    수정자 : 이준영
    내용 : 삭제가 안되어 핫 픽스, models에 맞게 다시 수정
    수정일 : 2023.07.10
    '''
    def delete(self, request, article_id):
            article = get_object_or_404(VocalNotice, id = article_id)
            # 본인이 작성한 게시글이 맞다면
            if request.user == article.user:
                article.delete()

            user = request.user
            one_day_passed = timezone.now() > (article.created_at + timedelta(days=1))

            if not one_day_passed:
                user_point = Point.objects.get(user=request.user)
                user_point.points -= 1000
                PointHistory.objects.create(user=user, point_change=-1000, reason="게시글 삭제")
                user_point.save()

                return Response({'message':'게시글이 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
                # 본인의 게시글이 아니라면
            else:
                return Response({'message':'본인 게시글만 삭제 가능합니다.'}, status=status.HTTP_403_FORBIDDEN)


#NoticeComment view
class NoticeCommentView(generics.ListCreateAPIView):
    # permission_classes = [AllowAny]
    permission_classes = [IsAuthenticatedOrReadOnly]
    '''
    작성자 :김은수
    내용 : 댓글의 생성과 조회가 가능함
    최초 작성일 : 2023.06.08
    업데이트 일자 : 2023.06.21
    '''
    queryset = NoticeComment.objects.all()
    serializer_class = NoticeCommentSerializer

    def get_queryset(self):
        article_id = self.kwargs['article_id']
        return NoticeComment.objects.filter(article_id=article_id)

    def get(self, request, *args, **kwargs):
        article_id = self.kwargs['article_id']
        comments = NoticeComment.objects.filter(article_id=article_id)
        comment_data = []
        
        for comment in comments:
            user = User.objects.get(id=comment.user_id)
            comment_good = comment.good.all()
            user_data = CommentUserSerializer(user).data
            serialzier = UserIdSerializer(comment_good, many=True)
            comment_data.append({
                'id': comment.id,
                'content':comment.content,
                'user': user_data,
                'good': serialzier.data
            })
        return Response(comment_data)
    
    def post(self, request, *args, **kwargs):
        serializer = NoticeCommentCreateSerializer(data=request.data)
        lookup_url_kwarg = 'article_id'
        article_id = self.kwargs.get(lookup_url_kwarg)
        article = VocalNotice.objects.get(id=article_id)

        if serializer.is_valid():
            serializer.save(user=request.user, article=article)

            user = request.user
            user_point = Point.objects.get(user=user)

            user_point.points += 500
            PointHistory.objects.create(user=user, point_change=+500, reason="댓글 작성")
            user_point.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class NoticeCommentViewByArticle(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [AllowAny]
    permission_classes = [IsAuthenticatedOrReadOnly]
    '''
    작성자 :김은수
    내용 : 댓글의 수정과 삭제가 가능함
    최초 작성일 : 2023.06.07
    업데이트 일자 : 2023.06.09
    '''  
    queryset = NoticeComment.objects.all()
    serializer_class = NoticeCommentCreateSerializer

class ArticleSearchView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    '''
    작성자 : 마동휘
    내용 : 게시글 검색
    최초 작성일 : 2023.06.22
    업데이트 일자 : 2023.07.02
    '''
    def get(self, request):
        query = request.GET.get('q')
        if query:
            articles = Article.objects.filter(Q(song_info__contains=query) | Q(comments__content__contains=query) | Q(voice__contains=query)).order_by('-created_at')
            vocal_notices = VocalNotice.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))

            article_serializer = ArticleSerializer(articles, many=True)
            vocal_notice_serializer = VocalNoticeSerializer(vocal_notices, many=True)

            response_data = {
                'articles': article_serializer.data,
                'vocal_notices': vocal_notice_serializer.data
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'message': '검색어를 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)
        
class VocalNoticeGoodView(APIView):
    def post(self,request,article_id):
        article = get_object_or_404(VocalNotice, id=article_id)
        if request.user in article.good.all():
            article.good.remove(request.user)
            return Response("좋아요를 취소하였습니다.", status=status.HTTP_200_OK)
        else:
            article.good.add(request.user)
            return Response("좋아요를 눌렀습니다.", status=status.HTTP_200_OK)
