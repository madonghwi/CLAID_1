from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'user'

urlpatterns = [
    path("signup/", views.UserSignupView.as_view(), name="signup"),
    path("user/", views.UserView.as_view(), name="user_view"),
    path("activate/<str:uidb64>/<str:token>/", views.UserActivate.as_view(), name="activate"),

    path("login/", views.CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", views.UserLogoutView.as_view(), name='logout'),

    path('google/', views.GoogleLogin.as_view(), name='googlelogin'),
    path('google/callback/', views.GoogleLogin.as_view(), name='googlelogin'),

    path('kakao/login/callback/', views.KakaoCallBackView.as_view(), name='kakaocallback'),
    path('kakao/<int:sns_id>/', views.KakaoUserView.as_view(), name='kakaologin'),    
    path('kakao/unlink/', views.KakaoUnLinkView.as_view()),    
    path('kakao/logout/', views.KakaoLogoutView.as_view()),
    path('follow/<int:user_id>/', views.FollowView.as_view(), name='follow_view'),
    path('profile/<int:user_id>/', views.ProfileAPIView.as_view(), name='profile_view'),

    path('points/', views.PointListCreateView.as_view(), name='points_list_create'),
    path('points/<int:user_id>/', views.PointDetailView.as_view(), name='points_detail'),
    path('history/', views.PointHistoryView.as_view(), name='point_history'),
]
