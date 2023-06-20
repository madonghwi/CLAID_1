from django.db import models
from rest_framework import serializers
from article.models import Article, Bookmark, Comment
from user.serializers import UserSerializer

class ArticleSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return {"pk": obj.user.pk, "login_type": obj.user.login_type, "nickname": obj.user.nickname, "profile_image": str(obj.user.profile_image)} 
    
    class Meta:
        model = Article
        fields = '__all__'

class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title', 'content', 'article_image', 'song')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class BookmarkSerializer(serializers.ModelSerializer):
# 작성자 : 마동휘
# 내용 : 북마크
# 최초 작성일 : 2023.06.12
# 업데이트 일자 : 2023.06.13
    user = UserSerializer()
    article = ArticleSerializer()

    class Meta:
        model = Bookmark
        fields = ('id', 'user', 'article')