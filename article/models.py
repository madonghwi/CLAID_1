from django.db import models
from user.models import User

class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    article_image = models.ImageField(upload_to='article/%Y/%m', blank=True)
    song = models.FileField(upload_to='songs/', blank=True)
    good = models.ManyToManyField(User, related_name='good_article',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #Tags = models.ManytoManyField(Tag, related_name='articles',blank=True)
    #Genre = models.ManytoManyField(Genre, related_name='articles',blank=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE,related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #good = models.ManyToManyField(User, related_name='good_comment',blank=True)

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE,related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} bookmarked {self.post.title}"