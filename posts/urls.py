from django.urls import path
from . import views

urlpatterns = [
    path('feed/create', views.create_post, name='create_post'),
    path('feed/create/send', views.create_post_view, name='send_post'),
    path('like/<int:post_id>/', views.like_post , name='like_post'),
    path('posts/<int:post_id>/comments/', views.post_comments, name='post_comments'),
    path('posts/<int:post_id>/add/', views.add_comment, name='add_comment')
]