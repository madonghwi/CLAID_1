from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArticleView.as_view(), name='article_view'),
    path('<int:user_id>/', views.ArticleDetailView.as_view(), name='article_detail_view'),
    path('bookmarks/', views.BookmarkCreate.as_view(), name='bookmark_create'),
    path('bookmarks/<int:pk>/', views.BookmarkDelete.as_view(), name='bookmark_destroy'),
    path('<int:article_id>/', views.ArticleDetailView.as_view(), name='article_detail_view'),
    path('<int:article_id>/good/',views.ArticleGoodView.as_view(), name='article_good_view'),
    path('commentcr/', views.CommentView.as_view(), name='CommentforTest'),
    path('commentud/<int:pk>/', views.CommentView.as_view(), name='CommentforTest'),
    path('commentud/<int:pk>/good/', views.CommentGoodView.as_view(), name='comment_good_view'),
    ]
