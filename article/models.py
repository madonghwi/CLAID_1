from django.db import models
from user.models import User
from django.utils import timezone
from datetime import datetime

class Article(models.Model):
    current_time = datetime.now()
    formatted_time = current_time.strftime("%H-%M-%S")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    article_image = models.ImageField(upload_to='article/%Y/%m/%d/'+formatted_time, null=True, blank=True)
    song = models.FileField(upload_to='songs/%Y/%m/%d/'+formatted_time)
    good = models.ManyToManyField(User, related_name='good_article',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #Tags = models.ManytoManyField(Tag, related_name='articles',blank=True)
    #Genre = models.ManytoManyField(Genre, related_name='articles',blank=True)
    hits = models.PositiveIntegerField(default=0)

    @property
    def click(self):
        self.hits +=1
        self.save()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE,related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    good = models.ManyToManyField(User, related_name='good_comment',blank=True)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class HitsCount(models.Model):
    ip = models.CharField(max_length=30)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    expire_date = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.ip