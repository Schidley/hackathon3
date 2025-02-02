from django.urls import path
from . import views
from .views import add_post
from .views import profile_view
from .views import PostListView
from .views import register
from .views import home_view, add_post

urlpatterns = [
    path('', views.home_view, name='home'),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('register/', register, name='register'),
    path('', views.home_view, name='home'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/add_comment/', views.add_comment, name='add_comment'),
    path('edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('add_post/', views.add_post, name='add_post'),  # Add this line
]


