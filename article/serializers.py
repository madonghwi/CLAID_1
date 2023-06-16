from django.db import models
from rest_framework import serializers
from article.models import Article
from article.models import Comment

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title', 'content', 'article_image', 'song')


class CommentSerializer(serializers.Serializer):
    class Meta:
        model = Comment
        fields = '__all__'

