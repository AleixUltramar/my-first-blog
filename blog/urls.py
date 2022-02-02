"""mysite URL Configuration"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListPostView.as_view(), name='post_list'),
    path('post/<int:pk>/', views.DetailPostView.as_view(), name='post_detail'),
    path('post/new/', views.CreatePostView.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', views.EditPostView.as_view(), name='post_edit'),
    path('post/<int:pk>/remove/', views.RemovePostView.as_view(), name='post_remove'),
]
