from django.urls import path
from .views import (
    PostListView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    PostLikesToggle,
    UserPostListView,
    CommentDeleteView
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', views.detail_view, name='post-detail'),
    path('post/<int:pk>/likes/', views.likes_toggle, name='post-likes'),
    path('user/<str:username>/post/<int:pk>/likes/', views.likes_toggle, name='user-posts-likes'),
    path('post/<int:pk>/comment/delete', CommentDeleteView.as_view(), name='delete-comment'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('test/', views.test, name='blog-test'),
    path('test/post/<int:pk>/', views.comment_create, name='test-comment')
]
