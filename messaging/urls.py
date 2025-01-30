from django.urls import path
from . import views
from .views import add_post
from .views import profile_view
from .views import PostListView
from .views import register

urlpatterns = [
    path('', views.home_view, name='home'),
    path('add_post/', add_post, name='add_post'),
    path('profile/', profile_view, name='profile'),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('register/', register, name='register'),
]




