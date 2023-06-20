from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArticleView.as_view(), name='article_view'),
    path('<int:article_id>/', views.ArticleDetailView.as_view(), name='article_detail_view'),
    path('<int:article_id>/good/',views.ArticleGoodView.as_view(), name='article_good_view'),
    path('<int:article_id>/commentcr/', views.CommentView.as_view(), name='CommentforTest'),
    path('<int:article_id>/commentud/<int:pk>/', views.CommentViewByArticle.as_view(), name='CommentforTest'),
    path('<int:article_id>/commentcr/<int:comment_id>/good/', views.CommentGoodView.as_view(), name='comment_good_view'),
]
