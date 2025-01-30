from django.urls import path
from . import views
from .views import add_post
from .views import profile_view
from .views import PostListView
from .views import register
from .views import home_view, add_post, edit_comment, delete_comment

urlpatterns = [
    path('', views.home_view, name='home'),
    path('add_post/', add_post, name='add_post'),
    path('profile/', profile_view, name='profile'),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('register/', register, name='register'),
    path('edit_comment/<int:comment_id>/', edit_comment, name='edit_comment'),
    path('delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),
]



