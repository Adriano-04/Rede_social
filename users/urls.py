from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('feed/', views.feed_view, name='feed' ),
    path('feed/edit/', views.edit_perfil, name='edit'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    path('api/register/', views.api_register, name='api_register'),
    path('api/login/', views.api_login, name='api_login'),
    path('follow/<int:user_id>/', views.follow_user, name='follow'),
    path('block/<int:user_id>/', views.block_user, name='block'),
    path('unblock/<int:user_id>/', views.unblock_user, name='unblock')
]