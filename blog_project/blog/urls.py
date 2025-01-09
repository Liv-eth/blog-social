from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from . import views
from . import api


# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'posts', api.PostViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_create, name='post_create'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='auth/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'),
         name='password_reset_complete'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_create, name='post_create'),
     path('comment/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
     path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
     path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
      path('search/', views.search, name='search'),
      path('notifications/', views.notifications, name='notifications'),
    path('notifications/<int:pk>/read/', views.mark_notification_read, name='mark_notification_read'),
    
      # API URLs
    path('api/', include(router.urls)),
    path('api/stats/', api.post_stats, name='post_stats'),
    
]