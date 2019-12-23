from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name = 'website-home'),
    path('blogs/', PostListView.as_view(), name = 'website-posts'),
    path('blogs/user/', UserPostListView.as_view(), name = 'website-userposts'),
    path('blog/<int:pk>/', PostDetailView.as_view(), name = 'website-postdetail'),
    path('blog/create/', PostCreateView.as_view(), name = 'website-postcreate'),
    path('blog/update/<int:pk>/', PostUpdateView.as_view(), name = 'website-postupdate'),
    path('blog/delete/<int:pk>/', PostDeleteView.as_view(), name = 'website-postdelete')
]
