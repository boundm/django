from django.urls import path, include
from .views import hello_world, article_list, add_article, edit_article, ArticleViewSet

from django.contrib.auth import views as auth_views
from . import views

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='article') 

urlpatterns = [
    path('', hello_world, name='home'), 
    path('articles/', article_list, name='article_list'), 
    path('articles/add/', add_article, name='add_article'),
    path('articles/edit/<int:article_id>/', edit_article, name='edit_article'), 

    path('register/', views.register, name='register'), 
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), 

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'), 
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'), 
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'), 
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'), 

    path('api/', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
   
]
