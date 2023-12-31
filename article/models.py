from django.db import models
from user.models import User
from django.utils import timezone
from datetime import datetime
from django.urls import reverse

class Article(models.Model):
    current_time = datetime.now()
    formatted_time = current_time.strftime("%H-%M-%S")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    voice = models.CharField(max_length=100)
    song_info = models.CharField(max_length=100) #원곡정보
    article_image = models.ImageField(upload_to='article/%Y/%m/%d/'+formatted_time, null=True, blank=True)
    song = models.FileField(upload_to='songs/%Y/%m/%d/'+formatted_time)
    good = models.ManyToManyField(User, related_name='good_article',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #Tags = models.ManytoManyField(Tag, related_name='articles',blank=True)
    #Genre = models.ManytoManyField(Genre, related_name='articles',blank=True)
    hits = models.BigIntegerField(default=0)

    def get_absolute_article_url(self):
        return reverse('article_detail_view', kwargs={"article_id":self.pk})
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



'''
수정자 : 이준영
내용 : 안쓰는 field 삭제, 핫픽스
업데이트 일자 : 2023.07.10
'''
# 방법공유
class VocalNotice(models.Model):
    current_time = datetime.now()
    formatted_time = current_time.strftime("%H-%M-%S")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hits = models.BigIntegerField(default=0)
    good = models.ManyToManyField(User, related_name='good_Notice',blank=True)

    def get_absolute_notice_url(self):
        return reverse('vocal_notice_detail_view', kwargs={"article_id":self.pk})

    @property
    def click(self):
        self.hits +=1
        self.save()

class NoticeComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(VocalNotice, on_delete=models.CASCADE,related_name='notice_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    good = models.ManyToManyField(User, related_name='notice_good_comment',blank=True)
        

class NoticeHitsCount(models.Model):
    ip = models.CharField(max_length=30)
    article = models.ForeignKey(VocalNotice, on_delete=models.CASCADE)
    expire_date = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.ip
